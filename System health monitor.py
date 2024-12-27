
import os
import psutil
import logging
from datetime import datetime

CPU_THRESHOLD = 80 
MEMORY_THRESHOLD = 80 
DISK_THRESHOLD = 80 

LOG_FILE = "/var/log/system_health.log"

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

def send_alert(message):
    print(message)
    logging.info(message)

def check_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1) 
    if cpu_usage > CPU_THRESHOLD:
        send_alert(f"WARNING: CPU usage is above threshold: {cpu_usage}%")
    return cpu_usage

def check_memory_usage():
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    if memory_usage > MEMORY_THRESHOLD:
        send_alert(f"WARNING: Memory usage is above threshold: {memory_usage}%")
    return memory_usage

def check_disk_usage():
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent
    if disk_usage > DISK_THRESHOLD:
        send_alert(f"WARNING: Disk usage is above threshold: {disk_usage}%")
    return disk_usage

def check_running_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        processes.append(proc.info)
    

    processes.sort(key=lambda x: x['memory_percent'], reverse=True)
    top_processes = processes[:5]
    send_alert("Top 5 processes by memory usage:")
    for proc in top_processes:
        send_alert(f"PID: {proc['pid']} - Name: {proc['name']} - CPU: {proc['cpu_percent']}% - Memory: {proc['memory_percent']}%")
    return top_processes

def monitor_system_health():
    check_cpu_usage()
    check_memory_usage()
    check_disk_usage()
    check_running_processes()

if __name__ == "__main__":
    monitor_system_health()
