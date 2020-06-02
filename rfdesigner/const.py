"""Generates constants for use in rfdesigner."""
MAJOR_VERSION = 0
MINOR_VERSION = 1
PATCH_VERSION = "0.rc0"

__version__ = f"{MAJOR_VERSION}.{MINOR_VERSION}.{PATCH_VERSION}"

REQUIRED_PYTHON_VER = (3, 5, 0)

PROJECT_GITHUB_USERNAME = "fronzbot"
PROJECT_GITHUB_REPOSITORY = "python-rfdesigner"

PROJECT_NAME = "rfdesigner"
PROJECT_PACKAGE_NAME = "python-rfdesigner"
PROJECT_LICENSE = "Apache-2.0"
PROJECT_AUTHOR = "Kevin Fronczak"
PROJECT_COPYRIGHT = f" 2020, {PROJECT_AUTHOR}"
PROJECT_URL = (
    f"https://github.com/{PROJECT_GITHUB_USERNAME}/{PROJECT_GITHUB_REPOSITORY}"
)
PROJECT_EMAIL = "kfronczak@gmail.com"
PROJECT_DESCRIPTION = "RF system budget/cascade analysis tool"
PROJECT_LONG_DESCRIPTION = "python-rfdesigner is a free tool to aid in RF system analysis and architecture feasibility."
PROJECT_CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Topic :: Scientific/Engineering",
]

PYPI_URL = f"https://pypi.python.org/pypi/{PROJECT_PACKAGE_NAME}"
