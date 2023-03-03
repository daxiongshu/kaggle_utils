import time
import datetime

def new_print(*x):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")

    print(timestamp, *x)

for i in range(10):
    new_print('hello',i)
    time.sleep(1)