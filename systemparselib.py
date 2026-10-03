import os

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
