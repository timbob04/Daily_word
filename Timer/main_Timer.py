def runTimer(timer_wrapper, dep):
    print("Timer running", end='')
    while True:
        dep.time.sleep(1)
        print('.', end='', flush=True)
