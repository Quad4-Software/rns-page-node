from setuptools import find_packages, setup

setup(
    name="rns-page-node",
    version="1.5.1",
    description="A simple way to serve pages and files over the Reticulum network.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sudo-Ivan",
    url="https://git.quad4.io/RNS-Things/page-node",
    packages=find_packages(),
    install_requires=[
        "rns>=1.1.9,<1.5.0",
        "cryptography>=47.0.0,<48",
    ],
    entry_points={
        "console_scripts": [
            "rns-page-node=rns_page_node.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires=">=3.9.2",
)
