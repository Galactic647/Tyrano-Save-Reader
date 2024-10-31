import threading
import ctypes


class KillableThread(threading.Thread):
    # It's bad but there's no other way.
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.killed = False

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id_, thread in threading._active.items():
            if thread is self:
                return id_

    def kill(self, auto_join=True):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadSate_SetAsyncExc(thread_id, 0)
        
        if auto_join:
            self.join()

    