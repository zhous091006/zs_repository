import threading
from abc import abstractmethod


class LibThreadWorker:
    def __init__(self):
        self._is_ready_to_quit = False

    @abstractmethod
    def run(self):
        pass

    def quit(self):
        self._is_ready_to_quit = True

    def is_ready_to_quit(self):
        return self._is_ready_to_quit


class LibObjectThread(threading.Thread):
    def __init__(self, worker_object: LibThreadWorker = None, name=None):
        super().__init__(name=name)
        self._worker_object: LibThreadWorker = worker_object

    def run(self) -> None:
        try:
            if self._worker_object:
                self._worker_object.run()
        finally:
            del self._worker_object

    def stop(self):
        try:
            self._worker_object.quit()
        except AttributeError:
            pass
