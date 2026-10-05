import os, subprocess, getpass, socket
from dataclasses import dataclass, asdict
from functools import cache

PCI_DEVICES = "/sys/bus/pci/devices"
PCI_IDS_PATHS = (
    "/usr/share/hwdata/pci.ids",
    "/usr/share/misc/pci.ids",
    "/usr/share/pci.ids",
)
VENDORS = {"10de": "NVIDIA", "1002": "AMD", "8086": "Intel"}

@dataclass
class GPU:
    vendor: str
    model: str
    driver: str | None = None

def _read_sysfs(path):
    try:
        with open(path) as f:
            return f.read().strip()
    except OSError:
        return None

@cache
def _load_pci_ids():
    """Returns {(vendor_id, device_id): name}"""
    names = {}
    for path in PCI_IDS_PATHS:
        try:
            f = open(path, encoding="utf-8", errors="replace")
        except OSError:
            continue
        with f:
            vendor = None
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                if line.startswith("C "):
                    break
                if line.startswith("\t\t"):
                    continue
                if line.startswith("\t"):
                    dev_id, _, name = line.strip().partition("  ")
                    if vendor:
                        names[(vendor, dev_id)] = name
                else:
                    vendor = line.split()[0]
        break
    return names

class Main():
    def __init__(self):
        def get_distro_info():
            if not os.path.exists('/etc/os-release'):
                return None

            info = {}

            with open('/etc/os-release') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        info[key] = value
            return info
        self.distro_info = get_distro_info()

    def get_distro_id(self):
        distro_id = self.distro_info.get('ID', '').strip('"')
        return distro_id
    
    def get_username(self):
        username = getpass.getuser()
        return username

    def get_kernel_version(self):
        kernel_version = os.uname().release
        return kernel_version

    def get_pretty_uptime(self):
        try:
            output = subprocess.check_output(['uptime', '-p'], text=True)
            return output.strip()
        except Exception as e:
            return f"Could not retrieve uptime: {e}"

    def get_session_type(self):
        session_type = os.getenv('XDG_SESSION_TYPE')
        if session_type:
            return session_type
        else:
            return "Could not retrieve session type."
    
    def get_hostname(self):
        hostname = socket.gethostname()
        return hostname

    def get_pretty_name(self):
        pretty_name = self.distro_info.get('PRETTY_NAME', '').strip('"')
        return pretty_name

    def get_de(self):
        desktop = os.environ.get("XDG_CURRENT_DESKTOP") or os.environ.get("DESKTOP_SESSION")
        if desktop:
            return desktop
        return None

    def get_cpu(self):
        cpu = ""
        try:
            with open("/proc/cpuinfo", "r", encoding="utf-8") as file:
                for line in file:
                    if "model name" in line.lower():
                        cpu = line.split(":", 1)[-1].strip()
                        break
        except FileNotFoundError:
            return None
        return cpu

    def get_gpu(self):
        gpus = []
        try:
            devices = sorted(os.listdir(PCI_DEVICES))
        except OSError:
            return gpus

        ids = _load_pci_ids()

        for dev in devices:
            base = os.path.join(PCI_DEVICES, dev)

            pci_class = _read_sysfs(base + "/class")
            if not pci_class or not pci_class.startswith("0x03"):
                continue

            vendor_id = (_read_sysfs(base + "/vendor") or "")[2:]
            device_id = (_read_sysfs(base + "/device") or "")[2:]

            vendor = VENDORS.get(vendor_id, vendor_id)

            name = ids.get((vendor_id, device_id), f"Device {device_id}")
            model = name.split('[')[-1].split(']')[0] if '[' in name else name

            driver = None
            if os.path.exists(base + "/driver"):
                driver = os.path.basename(os.path.realpath(base + "/driver"))

            gpus.append(GPU(vendor=vendor, model=model, driver=driver))

        return gpus
