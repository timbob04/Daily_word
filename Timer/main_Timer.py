def runTimer(timer_wrapper, dep):
    print("Timer running")
    timer_wrapper.request_start.emit("dailyWordApp")
    # dep.time.sleep(10)
    # timer_wrapper.request_shutdown.emit("dailyWordApp")
    # dep.time.sleep(2)
    print("Timer finished")