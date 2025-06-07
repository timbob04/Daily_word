def isProgramAlreadyRunning(server_name, dep):
    sock = dep.QLocalSocket()
    sock.connectToServer(server_name)
    running = sock.waitForConnected(100)
    sock.abort()
    return running    