import os, subprocess, getpass, socket

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
        return "Unknown"

    def get_cpu(self):
        cpu_result = subprocess.run(["lscpu"], capture_output=True, text=True)
        cpu_output = cpu_result.stdout

        cpu = ""

        for line in cpu_output.splitlines():
            if "Model name" in line:
                model = line.split(':')[-1].strip()
                cpu = model

    def get_gpu(self):
        result = subprocess.run(["lspci"], capture_output=True, text=True)
        output = result.stdout

        gpus = []

        for line in output.splitlines():
            if "VGA" in line:
                if "NVIDIA" in line:
                    model = line.split('[')[-1].split(']')[0]
                    gpus.append({'Vendor': 'NVIDIA', 'Model': model})
                elif "AMD" in line:
                    model = line.split('[')[-1].split(']')[0]
                    gpus.append({'Vendor': 'AMD', 'Model': model})
                elif "Intel" in line:
                    model = line.split('[')[-1].split(']')[0]
                    gpus.append({'Vendor': 'Intel', 'Model': model})
                pass
        return gpus

        return cpu
