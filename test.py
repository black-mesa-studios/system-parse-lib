import systemparselib

test = systemparselib.Main()

print(test.get_distro_id())
print(test.get_pretty_name())
print(test.get_de())
print(test.get_cpu())
print(test.get_gpu())
print(f"{test.get_username()}@{test.get_hostname()}")
print(test.get_kernel_version())
print(test.get_pretty_uptime())
print(test.get_session_type())
