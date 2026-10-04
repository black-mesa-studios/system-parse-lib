# system-parse-lib

A small Python library for reading system information on Linux: OS name, desktop environment, CPU and GPU models and vendors, and basic user details. One module, no third-party dependencies.

![License](https://img.shields.io/badge/license-BSD--3--Clause-blue)
![Python](https://img.shields.io/badge/python-3-yellow)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)

**Documentation:** https://black-mesa-studios.github.io/system-parse-lib/

## Features

- Distro ID and pretty name, read from `/etc/os-release`
- Current username and hostname
- Desktop environment, from `XDG_CURRENT_DESKTOP` or `DESKTOP_SESSION`
- CPU model, via `lscpu`
- GPU vendor and model (NVIDIA, AMD, Intel), via `lspci`

## Requirements

- Linux with an `/etc/os-release` file
- Python 3
- `lscpu` (util-linux) and `lspci` (pciutils)

## Installation

There's no package yet. Clone the repo and copy `systemparselib.py` next to your script:

```
git clone https://github.com/black-mesa-studios/system-parse-lib.git
cp system-parse-lib/systemparselib.py ./
```

## Usage

```python
import systemparselib

sysinfo = systemparselib.Main()

print(sysinfo.get_pretty_name())   # e.g. Arch Linux
print(sysinfo.get_de())            # e.g. KDE
print(sysinfo.get_cpu())           # e.g. AMD Ryzen 5 5600X 6-Core Processor
print(sysinfo.get_gpu())           # e.g. [{'Vendor': 'AMD', 'Model': '...'}]
print(f"{sysinfo.get_username()}@{sysinfo.get_hostname()}")
```

## Functions

All functions live on the `Main` class.

| Function | Returns | Description |
| --- | --- | --- |
| `get_distro_id()` | `str` | Short distro ID, like `arch` or `ubuntu` |
| `get_pretty_name()` | `str` | Human-readable OS name |
| `get_username()` | `str` | Current user's name |
| `get_hostname()` | `str` | Machine hostname |
| `get_de()` | `str` | Desktop environment, or `"Unknown"` if none is set |
| `get_cpu()` | `str` | CPU model name |
| `get_gpu()` | `list[dict]` | One `{'Vendor': ..., 'Model': ...}` per detected GPU |

Full details are in the [documentation](https://black-mesa-studios.github.io/system-parse-lib/).

## Testing

`test.py` prints the output of every function so you can check it on your machine:

```
python3 test.py
```

## License

Released under the [BSD 3-Clause License](LICENSE). Copyright 2026 Black Mesa Studios.
