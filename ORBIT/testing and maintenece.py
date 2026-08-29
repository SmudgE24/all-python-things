import psutil
import cpuinfo
import platform

print("CPU:", cpuinfo.get_cpu_info()["brand_raw"])
print("CPU Usage:", psutil.cpu_percent(), "%")
print("RAM Usage:", psutil.virtual_memory().percent, "%")
print("Disk Usage:", psutil.disk_usage("/").percent, "%")
print("OS:", platform.system(), platform.release())
print("Architecture:", platform.machine())

for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
    print(process.info)