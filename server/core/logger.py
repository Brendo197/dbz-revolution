class ServerLogger:
    def __init__(self):
        self.logs = []

    def log(self, message):
        print(message)
        self.logs.append(message)

        # mantém só últimos 500 logs
        if len(self.logs) > 500:
            self.logs.pop(0)


logger = ServerLogger()