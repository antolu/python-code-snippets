"""
This module contains the TaskLock class.
The TaskLock class is intended to be used for when multiple
threads are running tasks that need to be completed before
the main thread can continue. The main thread can call
TaskLock.wait() to wait for all tasks to complete.
"""


import threading


class TaskLock:
    """
    This class is used to wait for multiple tasks to complete.

    This class can be useful when a scope does not have access to
    the subthread handles and the main thread needs to wait for all
    subthreads to complete before continuing. For instance the
    register() method can be called during synchronous execution,
    while the unregister() method can be called during an asynchronous
    callback that is completely isolated from the main thread.

    Usage example:
    >>> lock = TaskLock()
    >>>
    >>> def foo():
    >>>     lock.register()
    >>>     # do something
    >>>     lock.unregister()
    >>>
    >>> def bar():
    >>>     lock.register()
    >>>     # do something
    >>>     lock.unregister()
    >>>
    >>> # start threads
    >>> threading.Thread(target=foo).start()
    >>> threading.Thread(target=bar).start()
    >>>
    >>> # wait for threads to complete
    >>> lock.wait()
    >>>
    >>> # finished
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._event_counter = 0

        self._event = threading.Event()

    def register(self):
        """
        Increment the event counter by one.
        """
        with self._lock:
            self._event_counter += 1

    def unregister(self):
        """
        Decrement the event counter by one.

        If the event counter reaches zero, the notify event.
        """
        with self._lock:
            self._event_counter -= 1

            if self._event_counter == 0:
                self._event.set()

    def wait(self):
        """
        Block until the event counter reaches zero.
        """
        self._event.wait()
        self._event.clear()

    def reset(self):
        """
        Reset the event counter to zero.
        """
        self._event.clear()
        self._event_counter = 0
