import time

def memory_spike():
    big_list = []
    try:
        while True:
            big_list.append('x' * 1000000)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Memory spike stopped manually.")
memory_spike()