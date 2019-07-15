"""
Simple rollback mechanism usable as a context manager and/or instance methods.
"""


class Rollback(object):
    """
    Provides rollback methods and context manager
    """

    __slots__ = ("steps", "onError", "onSuccess", "raiseError")

    def __init__(self, onError=False, onSuccess=False, raiseError=True):
        """
        :onError:    Within a context manager, call `doRollback` if an
                     exception is raised.
        :onSuccess:  Within a context manager, call `doRollback` if *no*
                     exception is raised.
        :raiseError: Within a context manager, if an exception is raised,
                     re-raise upon exiting the context manager block.
                     *NOTE:* any exceptions from rollback steps are
                     immediately raised, regardless of this parameter.
        """
        self.steps = []
        self.onError = onError
        self.onSuccess = onSuccess
        self.raiseError = raiseError

    def __enter__(self):
        """
        Called when entering a context manager block. Returned value is
        assigned to the `as` statement (if specified).
        """
        return self

    @staticmethod
    def _frames(traceback):
        """
        Returns generator that iterates over frames in a traceback
        """
        frame = traceback
        while frame.tb_next:
            frame = frame.tb_next
            yield frame.tb_frame
        return

    def _methodInTraceback(self, name, traceback):
        """
        Returns boolean whether traceback contains method from this instance
        """
        foundMethod = False
        for frame in self._frames(traceback):
            this = frame.f_locals.get("self")
            if this is self and frame.f_code.co_name == name:
                foundMethod = True
                break
        return foundMethod

    def __exit__(self, exceptionType, exceptionValue, traceback):
        """
        Called when exiting a context manager block. If no exception was
        raised, all arguments apart from self will be `None`. The return
        value indicates what should happen next if an exception was raised.
        A value of `True` means an exception should be suppressed and `False`
        means the exception should be re-raised.
        """
        error = bool(traceback is not None)
        suppressError = not self.raiseError
        if (error and self.onError) or (self.onSuccess and not error):
            self.doRollback()
        if error and suppressError:
            # if doRollback is called manually _and_ raiseError is False,
            # don't suppress error from any rollback steps that are called.
            suppressError = not self._methodInTraceback("doRollback", traceback)
        return suppressError

    def addStep(self, callback, *args, **kwargs):
        """
        Add rollback step with optional arguments. If a rollback is
        triggered, each step is called in LIFO order.
        """
        self.steps.append((callback, args, kwargs))

    def clearSteps(self):
        """
        Clears all rollback steps.
        """
        self.steps[:] = []

    def doRollback(self):
        """
        Call each rollback step in LIFO order.
        """
        while self.steps:
            callback, args, kwargs = self.steps.pop()
            callback(*args, **kwargs)
