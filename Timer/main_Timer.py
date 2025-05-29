def runTimer(timer_wrapper, dep):
    print("Timer running")
    while True:
        dep.time.sleep(1)
    # timer_wrapper.request_start.emit("dailyWordApp")
    # dep.time.sleep(10)
    # timer_wrapper.request_shutdown.emit("dailyWordApp")
    # dep.time.sleep(2)
    # print("Timer finished")
    timer_wrapper.timerRunning = False