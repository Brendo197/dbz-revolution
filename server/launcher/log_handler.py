import logging
import queue

log_queue = queue.Queue()

class QueueHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        log_queue.put(msg)


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s: %(message)s"
    )

    # Arquivo
    file_handler = logging.FileHandler("logs/server.log", encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Fila (para GUI)
    queue_handler = QueueHandler()
    queue_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(queue_handler)

    return log_queue
