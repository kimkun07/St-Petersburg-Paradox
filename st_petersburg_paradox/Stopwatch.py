import time


class Stopwatch:
    def __init__(self):
        self._start_time = None
        self._stop_time = None

    def start(self):
        self._start_time = time.time()

    def stop(self):
        self._stop_time = time.time()

    def elapsed_time(self):
        assert self._start_time is not None and self._stop_time is not None
        return self._stop_time - self._start_time

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return True
