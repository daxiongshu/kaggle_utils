import subprocess
import psutil
import time
import datetime

import matplotlib.pyplot as plt
import seaborn
seaborn.set_style('darkgrid')

def plot(ts,ms):
    plt.plot(ts,ms)
    # show timestamp on x-axis every 3 seconds
    plt.xticks(ts[::30])
    plt.ylabel('GB')
    plt.xlabel('timestamp')
    plt.savefig('./log/mem.png', bbox_inches='tight')

def convert_pid(pid):
    # Get the process ID (PID) of the other script
    if isinstance(pid,int):
        pid = psutil.Process(pid)
    if not isinstance(pid,psutil.Process):
        raise TypeError(f'wrong pid type: {type(pid)}')
    return pid

def monitor_memory(pid,t=.1,output='./log/mem.log'):
    # pid to monitor
    pid = convert_pid(pid)
    # Loop until the other script is finished
    mems = []
    ts = []
    with open(output,'w') as fo:
        while True:
            # Wait for the monitoring interval
            time.sleep(t)
            
            # Get the current memory usage of the other script
            memory_current = pid.memory_info().rss / 1024 / 1024 / 1024
            mems.append(memory_current)
            
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            ts.append(f'{timestamp}')
            # Print the memory usage
            fo.write(f"{timestamp} Memory used: {memory_current:.2f} GB\n")
            
            # Exit the loop if the other script has finished
            if not psutil.pid_exists(pid.pid) or pid.status()=='zombie':
                break
    plot(ts,mems)

def run_script(script_path):
    process = subprocess.Popen(["python", script_path], stdout=subprocess.PIPE)
    pid = psutil.Process(process.pid)
    monitor_memory(pid)

    # Open a file for writing the standard output stream
    with open("./log/stdout.log", "w") as output_file:
        # Read the contents of the standard output stream
        while True:
            stdout_line = process.stdout.readline()
            if not stdout_line:
                break

            # Write the timestamp and the stdout_line to the file
            output_file.write(f"{stdout_line.decode()}")
