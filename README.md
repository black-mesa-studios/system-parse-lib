# system-parse-lib

A small Python library for reading system information on Linux: OS name, kernel version, uptime, desktop environment, session type, CPU and GPU models and vendors, and basic user details. One module, no third-party dependencies, and no external commands: everything is read from `/etc`, `/proc` and `/sys`.

![License](https://img.shields.io/badge/license-BSD--3--Clause-blue)
![Python](https://img.shields.io/badge/python-3-yellow)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)

**Documentation:** https://black-mesa-studios.github.io/system-parse-lib/

## Features

- Distro ID and pretty name, read from `/etc/os-release`
- Current username and hostname
- Kernel version and uptime (as seconds or readable text)
- Desktop environment, from `XDG_CURRENT_DESKTOP` or `DESKTOP_SESSION`
- Session type (Wayland, X11, tty), from `XDG_SESSION_TYPE`
- CPU model, from `/proc/cpuinfo`
- GPUs with vendor, model and kernel driver, from `/sys/bus/pci/devices`

## Requirements

- Linux
- Python 3.10 or newer
- Optional: a `pci.ids` file (from the `hwdata` or `pciids` package) so `get_gpu()` can show real model names

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
print(sysinfo.get_session_type())  # e.g. wayland
print(sysinfo.get_kernel_version())  # e.g. 6.11.2-arch1-1
print(sysinfo.get_pretty_uptime())   # e.g. up 3 hours, 12 minutes
print(sysinfo.get_cpu())           # e.g. AMD Ryzen 5 5600X 6-Core Processor
print(sysinfo.get_gpu())           # e.g. [GPU(vendor='AMD', model='...', driver='amdgpu')]
print(f"{sysinfo.get_username()}@{sysinfo.get_hostname()}")
```

## Functions

All functions live on the `Main` class.

| Function | Returns | Description |
| --- | --- | --- |
| `get_distro_id()` | `str \| None` | Short distro ID, like `arch` or `ubuntu` |
| `get_pretty_name()` | `str \| None` | Human-readable OS name |
| `get_username()` | `str` | Current user's name |
| `get_hostname()` | `str` | Machine hostname |
| `get_de()` | `str \| None` | Desktop environment, or `None` if none is set |
| `get_session_type()` | `str` | Session type from `XDG_SESSION_TYPE`, like `wayland` or `x11` |
| `get_kernel_version()` | `str` | Kernel release, like `6.11.2-arch1-1` |
| `get_uptime_seconds()` | `int \| None` | Seconds since boot |
| `get_pretty_uptime()` | `str \| None` | Readable uptime, like `up 3 hours, 12 minutes` |
| `get_cpu()` | `str \| None` | CPU model name |
| `get_gpu()` | `list[GPU]` | One `GPU(vendor, model, driver)` per display device |

Full details are in the [documentation](https://black-mesa-studios.github.io/system-parse-lib/).

## Testing

`test.py` prints the output of every function so you can check it on your machine:

```
python3 test.py
```

## License

Released under the [BSD 3-Clause License](LICENSE). Copyright 2026 Black Mesa Studios.
