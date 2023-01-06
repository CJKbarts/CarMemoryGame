import time


def countdown(t):
    while t:
        print("\r", t, end="")
        time.sleep(1)
        t -= 1
    print(end='\r')
    print('Begin!')
