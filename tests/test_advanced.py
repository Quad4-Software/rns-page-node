#!/usr/bin/env python3
import random
import shutil
import string
import threading
import time
import tracemalloc
import unittest
from pathlib import Path

import RNS

from rns_page_node import PageNode


class AdvancedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = Path("./test_advanced_tmp")
        cls.test_dir.mkdir(exist_ok=True)
        cls.pages_dir = cls.test_dir / "pages"
        cls.files_dir = cls.test_dir / "files"
        cls.identity_dir = cls.test_dir / "node-config"

        cls.pages_dir.mkdir(exist_ok=True)
        cls.files_dir.mkdir(exist_ok=True)
        cls.identity_dir.mkdir(exist_ok=True)

        # Create test files
        (cls.pages_dir / "index.mu").write_text("Hello World")
        (cls.files_dir / "test.txt").write_bytes(b"File content")

        # Initialize RNS
        RNS.Reticulum(str(cls.test_dir / "config"))
        cls.identity = RNS.Identity()

        cls.node = PageNode(
            cls.identity,
            str(cls.pages_dir),
            str(cls.files_dir),
            announce_interval=0,
        )

    @classmethod
    def tearDownClass(cls):
        cls.node.shutdown()
        # Small sleep to allow threads to exit
        time.sleep(0.5)
        shutil.rmtree(cls.test_dir, ignore_errors=True)

    def test_smoke(self):
        """Basic smoke test to ensure node is initialized and has handlers."""
        self.assertIsNotNone(self.node.destination)
        self.assertTrue(len(self.node.servedpages) >= 1)

    def test_performance(self):
        """Measure performance of request handlers."""
        start_time = time.time()
        iterations = 100
        for _ in range(iterations):
            # Simulate a request to serve_page
            self.node.serve_page("/page/index.mu", None, None, None, None, None)

        duration = time.time() - start_time
        avg_time = duration / iterations
        print(
            f"\n[Performance] Avg serve_page time: {avg_time:.6f}s over {iterations} iterations",
        )
        self.assertLess(avg_time, 0.01, "Performance too slow")

    def test_leaks(self):
        """Test for memory and thread leaks."""
        tracemalloc.start()
        initial_threads = threading.active_count()

        # Perform some operations
        for _ in range(50):
            self.node.register_pages()
            self.node.register_files()
            self.node.serve_page("/page/index.mu", None, None, None, None, None)

        current_threads = threading.active_count()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"\n[Leak Test] Peak memory: {peak / 1024 / 1024:.2f} MB")
        print(f"[Leak Test] Thread count change: {current_threads - initial_threads}")

        # Allow some thread variation but not excessive growth
        self.assertLessEqual(
            current_threads,
            initial_threads + 5,
            "Potential thread leak detected",
        )

    def test_fuzzing(self):
        """Fuzz request handlers with random inputs."""
        print("\n[Fuzzing] Starting fuzzing of request handlers...")
        for _ in range(100):
            # Random path fuzzing
            random_path = "/" + "".join(
                random.choices(string.ascii_letters + string.digits + "/.", k=20),
            )
            # Should not crash
            self.node.serve_page(random_path, None, None, None, None, None)
            res_f = self.node.serve_file(random_path, None, None, None, None, None)

            # Close file handles if returned to avoid ResourceWarnings
            if (
                isinstance(res_f, list)
                and len(res_f) > 0
                and hasattr(res_f[0], "close")
            ):
                res_f[0].close()

            # Random data fuzzing
            random_data = {
                "field_" + "".join(random.choices(string.ascii_letters, k=5)): "".join(
                    random.choices(string.ascii_letters + string.digits, k=20),
                )
                for _ in range(3)
            }
            self.node.serve_page("/page/index.mu", random_data, None, None, None, None)

    def test_property_based(self):
        """Path traversal blocked; file responses are list or denied bytes."""
        traversal_paths = [
            "/page/../../etc/passwd",
            "/page/../main.py",
            "/page/./index.mu/../../../",
        ]
        for path in traversal_paths:
            response = self.node.serve_page(path, None, None, None, None, None)
            self.assertIn(
                b"Not Allowed",
                response,
                f"Path traversal succeeded for {path}",
            )

        response = self.node.serve_file("/file/test.txt", None, None, None, None, None)
        try:
            self.assertTrue(isinstance(response, list) or isinstance(response, bytes))
            if isinstance(response, list):
                self.assertEqual(len(response), 2)
                self.assertTrue(hasattr(response[0], "read"))
        finally:
            if (
                isinstance(response, list)
                and len(response) > 0
                and hasattr(response[0], "close")
            ):
                response[0].close()

    def test_property_config_loading(self):
        """Property-based testing for configuration loading."""
        from rns_page_node import load_config

        config_file = self.test_dir / "prop_config"

        for _ in range(50):
            # Generate random valid and invalid config lines
            expected = {}
            lines = []
            for i in range(10):
                if random.random() > 0.3:
                    # Valid line
                    key = (
                        f"key_{i}_{''.join(random.choices(string.ascii_letters, k=5))}"
                    )
                    val = (
                        f"val_{i}_{''.join(random.choices(string.ascii_letters, k=5))}"
                    )
                    lines.append(f"{key} = {val}")
                    expected[key] = val
                # Invalid line (comment or no =)
                elif random.random() > 0.5:
                    lines.append(
                        f"# comment {''.join(random.choices(string.ascii_letters, k=10))}",
                    )
                else:
                    lines.append(
                        "".join(random.choices(string.ascii_letters, k=15)),
                    )

            config_file.write_text("\n".join(lines))
            loaded = load_config(str(config_file))
            self.assertEqual(loaded, expected)

    def test_property_scanning(self):
        """Property-based testing for directory scanning."""
        scan_test_dir = self.test_dir / "scan_test"
        if scan_test_dir.exists():
            shutil.rmtree(scan_test_dir)
        scan_test_dir.mkdir()

        expected_pages = []
        expected_files = []

        for i in range(20):
            name = "".join(random.choices(string.ascii_letters, k=8))
            if random.random() > 0.5:
                # Page scenario
                if random.random() > 0.2:
                    # Normal page
                    f = scan_test_dir / f"{name}.mu"
                    f.touch()
                    expected_pages.append(str(f))
                else:
                    # .allowed file (should be ignored by pages)
                    f = scan_test_dir / f"{name}.allowed"
                    f.touch()
            # File scenario
            elif random.random() > 0.2:
                # Normal file
                f = scan_test_dir / name
                f.touch()
                expected_files.append(str(f))
            else:
                # Hidden file (should be ignored by both)
                f = scan_test_dir / f".{name}"
                f.touch()

        # We need to test the methods on a PageNode instance
        # Pages scan
        found_pages = self.node._scan_pages(str(scan_test_dir))
        self.assertCountEqual(found_pages, expected_pages)

        # Files scan (files scan includes .mu files too as they are just files)
        # but excludes hidden files.
        found_files = self.node._scan_files(str(scan_test_dir))
        # Our expected_files only tracked "normal" files, but _scan_files
        # includes everything that isn't hidden and isn't a directory.
        actual_expected_files = [
            str(f)
            for f in scan_test_dir.iterdir()
            if not f.name.startswith(".") and f.is_file()
        ]
        self.assertCountEqual(found_files, actual_expected_files)

    def test_property_script_execution(self):
        """Property-based testing for script execution vs reading."""
        script_path = self.pages_dir / "prop_script.mu"

        # Property: File with shebang AND executable bit -> Executed
        script_path.write_text("#!/bin/sh\necho 'script output'")
        script_path.chmod(0o755)
        response = self.node.serve_page(
            "/page/prop_script.mu",
            None,
            None,
            None,
            None,
            None,
        )
        self.assertEqual(response.strip(), b"script output")

        # Property: File with shebang but NO executable bit -> Read as text
        script_path.chmod(0o644)
        response = self.node.serve_page(
            "/page/prop_script.mu",
            None,
            None,
            None,
            None,
            None,
        )
        self.assertIn(b"#!/bin/sh", response)

        # Property: File without shebang -> Read as text even if executable
        script_path.write_text("plain text content")
        script_path.chmod(0o755)
        response = self.node.serve_page(
            "/page/prop_script.mu",
            None,
            None,
            None,
            None,
            None,
        )
        self.assertEqual(response, b"plain text content")


if __name__ == "__main__":
    unittest.main()
