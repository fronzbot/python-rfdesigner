"""Generates constants for use in rfdesigner."""
MAJOR_VERSION = 0
MINOR_VERSION = 1
PATCH_VERSION = "0.rc0"

__version__ = f"{MAJOR_VERSION}.{MINOR_VERSION}.{PATCH_VERSION}"

# System constants
KBOLTZMAN = 1.38e-23

# General attributes
# Property name, Description, Units
ATTR_CONTROL = ["control", "Control voltage", "V"]
ATTR_F3DB = ["f3db", "Dominant pole frequency of the block (3dB roll-off)", "MHz"]
ATTR_FBW = ["fbw", "Cutoff frequency of the block", "MHz"]
ATTR_GAIN = ["gain", "Gain of the block", "dB"]
ATTR_GAIN_MAX = ["gain_max", "Maximum block gain", "dB"]
ATTR_GAIN_MIN = ["gain_min", "Minimum block gain", "dB"]
ATTR_GAIN_STEP = ["gain_step", "Gain control step/LSB", "dB"]
ATTR_IIP3 = ["iip3", "Input 3rd-order intercept", "dBm"]
ATTR_LAW = ["law", "Detector law", "log/square/rms"]
ATTR_MDS = ["mds", "Minimum detectable signal", "dBm"]
ATTR_NAME = ["name", "Name of block (for example, a part name)", ""]
ATTR_NF = ["nf", "Noise figure of the block", "dB"]
ATTR_OIP3 = ["oip3", "Output 3rd-order intercept", "dBm"]
ATTR_P1DB = ["p1db", "Output 1dB Compression point", "dBm"]
ATTR_POWER = ["power", "Power consumption of the block", "W"]
ATTR_SMAX = ["smax", "Maximum input signal", "dBm"]

# Project package variable
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
