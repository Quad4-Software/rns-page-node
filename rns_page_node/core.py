"""PageNode: register .mu pages and files on an RNS destination."""

import threading
import time
from pathlib import Path
from typing import Any, List, Optional, Union

import RNS

from .handlers import serve_default_index, serve_file, serve_page


class PageNode:
    """Serves .mu pages and static files from disk over a single RNS destination."""

    def __init__(
        self,
        identity: RNS.Identity,
        pagespath: str,
        filespath: str,
        announce_interval: int = 360,
        name: Optional[str] = None,
        page_refresh_interval: int = 0,
        file_refresh_interval: int = 0,
    ) -> None:
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self.identity = identity
        self.name = name
        self.pagespath = Path(pagespath)
        self.filespath = Path(filespath)
        self.destination = RNS.Destination(
            identity,
            RNS.Destination.IN,
            RNS.Destination.SINGLE,
            "nomadnetwork",
            "node",
        )
        self.announce_interval = announce_interval
        self.last_announce: float = 0
        self.page_refresh_interval = page_refresh_interval
        self.file_refresh_interval = file_refresh_interval
        self.last_page_refresh = time.time()
        self.last_file_refresh = time.time()
        self.servedpages: List[str] = []
        self.servedfiles: List[str] = []

        self.register_pages()
        self.register_files()

        self.destination.set_link_established_callback(self.on_connect)

        self._announce_thread = threading.Thread(
            target=self._announce_loop,
            daemon=True,
        )
        self._announce_thread.start()
        self._refresh_thread = threading.Thread(target=self._refresh_loop, daemon=True)
        self._refresh_thread.start()

    def serve_page(
        self,
        path: str,
        data: Any,
        request_id: bytes,
        link_id: Optional[bytes],
        remote_identity: Any,
        requested_at: float,
    ) -> bytes:
        return serve_page(
            path,
            data,
            request_id,
            link_id,
            remote_identity,
            requested_at,
            self.pagespath,
        )

    def serve_file(
        self,
        path: str,
        data: Any,
        request_id: bytes,
        link_id: bytes,
        remote_identity: Any,
        requested_at: float,
    ) -> Any:
        return serve_file(
            path,
            data,
            request_id,
            link_id,
            remote_identity,
            requested_at,
            self.filespath,
        )

    def register_pages(self) -> None:
        pages = self._scan_pages(self.pagespath)

        with self._lock:
            self.servedpages = pages

        pages_path_obj = self.pagespath.resolve()

        if not (pages_path_obj / "index.mu").is_file():
            self.destination.register_request_handler(
                "/page/index.mu",
                response_generator=serve_default_index,
                allow=RNS.Destination.ALLOW_ALL,
            )

        for full_path in pages:
            page_path = Path(full_path).resolve()
            try:
                rel = page_path.relative_to(pages_path_obj).as_posix()
            except ValueError:
                continue
            request_path = f"/page/{rel}"
            self.destination.register_request_handler(
                request_path,
                response_generator=self.serve_page,
                allow=RNS.Destination.ALLOW_ALL,
            )

    def register_files(self) -> None:
        files = self._scan_files(self.filespath)

        with self._lock:
            self.servedfiles = files

        files_path_obj = self.filespath.resolve()

        for full_path in files:
            file_path = Path(full_path).resolve()
            try:
                rel = file_path.relative_to(files_path_obj).as_posix()
            except ValueError:
                continue
            request_path = f"/file/{rel}"
            self.destination.register_request_handler(
                request_path,
                response_generator=self.serve_file,
                allow=RNS.Destination.ALLOW_ALL,
                auto_compress=32_000_000,
            )

    def _scan_pages(self, base: Union[Path, str]) -> List[str]:
        if isinstance(base, str):
            base = Path(base)
        if not base.exists():
            return []
        served: List[str] = []
        for entry in base.iterdir():
            if entry.name.startswith("."):
                continue
            if entry.is_dir():
                served.extend(self._scan_pages(entry))
            elif entry.is_file() and entry.name.endswith(".mu"):
                served.append(str(entry))
        return served

    def _scan_files(self, base: Union[Path, str]) -> List[str]:
        if isinstance(base, str):
            base = Path(base)
        if not base.exists():
            return []
        served: List[str] = []
        for entry in base.iterdir():
            if entry.name.startswith("."):
                continue
            if entry.is_dir():
                served.extend(self._scan_files(entry))
            elif entry.is_file():
                served.append(str(entry))
        return served

    def on_connect(self, _link: Any) -> None:
        pass

    def _announce_loop(self) -> None:
        interval_seconds = max(self.announce_interval, 0) * 60
        try:
            while not self._stop_event.is_set():
                now = time.time()
                if (
                    self.last_announce == 0
                    or now - self.last_announce >= interval_seconds
                ):
                    try:
                        if self.name:
                            self.destination.announce(
                                app_data=self.name.encode("utf-8"),
                            )
                        else:
                            self.destination.announce()
                        self.last_announce = time.time()
                    except (TypeError, ValueError) as announce_error:
                        RNS.log(
                            f"Error during announce: {announce_error}",
                            RNS.LOG_ERROR,
                        )
                wait_time = max(
                    (self.last_announce + interval_seconds) - time.time()
                    if self.last_announce
                    else 0,
                    1,
                )
                self._stop_event.wait(min(wait_time, 60))
        except Exception as e:
            RNS.log(f"Error in announce loop: {e}", RNS.LOG_ERROR)

    def _refresh_loop(self) -> None:
        try:
            while not self._stop_event.is_set():
                now = time.time()
                if (
                    self.page_refresh_interval > 0
                    and now - self.last_page_refresh >= self.page_refresh_interval
                ):
                    self.register_pages()
                    self.last_page_refresh = time.time()
                if (
                    self.file_refresh_interval > 0
                    and now - self.last_file_refresh >= self.file_refresh_interval
                ):
                    self.register_files()
                    self.last_file_refresh = time.time()

                wait_candidates: List[float] = []
                if self.page_refresh_interval > 0:
                    wait_candidates.append(
                        max(
                            (self.last_page_refresh + self.page_refresh_interval)
                            - time.time(),
                            0.5,
                        ),
                    )
                if self.file_refresh_interval > 0:
                    wait_candidates.append(
                        max(
                            (self.last_file_refresh + self.file_refresh_interval)
                            - time.time(),
                            0.5,
                        ),
                    )

                wait_time = min(wait_candidates) if wait_candidates else 1.0
                self._stop_event.wait(min(wait_time, 60))
        except Exception as e:
            RNS.log(f"Error in refresh loop: {e}", RNS.LOG_ERROR)

    def shutdown(self) -> None:
        RNS.log("Shutting down PageNode...", RNS.LOG_INFO)
        self._stop_event.set()
        try:
            self._announce_thread.join(timeout=5)
            self._refresh_thread.join(timeout=5)
        except Exception as e:
            RNS.log(f"Error waiting for threads to shut down: {e}", RNS.LOG_ERROR)
        try:
            if hasattr(self.destination, "close"):
                self.destination.close()
        except Exception as e:
            RNS.log(f"Error closing RNS destination: {e}", RNS.LOG_ERROR)
