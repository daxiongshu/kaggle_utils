import sys
from pid_monitor import run_script

if __name__ == '__main__':
    # Start the other Python script
    script_path = sys.argv[1]
    run_script(script_path)