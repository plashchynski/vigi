"""
A script to profile the CPU and memory usage of a program over time
requires the psutil library to be installed (pip install psutil)

Usage:
    
    sudo python cpu_mem_profiler.py <pid>

Where <pid> is the process ID of the program you want to profile.
"""

import sys
import time

import psutil
import matplotlib.pyplot as plt


# Lists to hold the data
cpu_percentages = []
memory_usage = []

# get pid from command line argument
pid = int(sys.argv[1])

# Get the process
process = psutil.Process(pid)


# Monitoring interval (seconds)
INTERVAL = 1
DURATION = 120  # How long to monitor (seconds)

for _ in range(int(DURATION / INTERVAL)):
    # Record the current CPU and memory utilization
    cpu_percentages.append(process.cpu_percent())
    uss = process.memory_full_info().uss / 1024 /1024 # Convert to Mb

    memory_usage.append(uss)

    # Wait for the next interval
    time.sleep(INTERVAL)

# Plot two subplots for CPU and memory usage
fig, ax1 = plt.subplots()

CPU_COLOR = 'tab:red'
ax1.set_xlabel('Time (seconds)')
ax1.set_ylabel('CPU Usage (%)', color=CPU_COLOR)
ax1.plot(cpu_percentages, color=CPU_COLOR)
ax1.tick_params(axis='y', labelcolor=CPU_COLOR)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
MEM_COLOR = 'tab:blue'
ax2.set_xlabel('Time (seconds)')
ax2.set_ylabel('Memory Usage (Mb)', color=MEM_COLOR)  # we already handled the x-label with ax1
ax2.plot(memory_usage, color=MEM_COLOR)
ax2.tick_params(axis='y', labelcolor=MEM_COLOR)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.title('CPU and Memory Usage Over Time')
plt.savefig('cpu_mem_profile.png')
