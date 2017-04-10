'''
Simple rollback mechanism usable as a context manager and/or instance methods.
'''

class Rollback(object):
  '''
  Provides rollback methods and context manager
  '''
  __slots__ = ('steps', 'onError', 'onSuccess', 'raiseError')

  def __init__(self, onError=False, onSuccess=False, raiseError=True):
    '''
    :onError:    Within a context manager, call `doRollback` if an
                 exception is raised.
    :onSuccess:  Within a context manager, call `doRollback` if *no*
                 exception is raised.
    :raiseError: Within a context manager, if an exception is raised,
                 re-raise upon exiting the context manager block.
                 *NOTE:* any exceptions from rollback steps are
                 immediately raised, regardless of this parameter.
    '''
    self.steps = []
    self.onError = onError
    self.onSuccess = onSuccess
    self.raiseError = raiseError

  def __enter__(self):
    '''
    Called when entering a context manager block. Returned value is
    assigned to the `as` statement (if specified).
    '''
    return self

  def __exit__(self, exceptionType, exceptionValue, traceback):
    '''
    Called when exiting context manager block. If no exception was
    raised, all arguments apart from self will be `None`.
    '''
    error = True
    if exceptionType is None and exceptionValue is None and traceback is None:
      error = False
    if (error and self.onError) or (self.onSuccess and not error):
      self.doRollback()
    return not self.raiseError

  def addStep(self, callback, *args, **kwargs):
    '''
    Add rollback step with optional arguments. If a rollback is
    triggered, each step is called in LIFO order.
    '''
    self.steps.append((callback, args, kwargs))

  def clearSteps(self):
    '''
    Clears all rollback steps.
    '''
    self.steps[:] = []

  def doRollback(self):
    '''
    Call each rollback step in LIFO order.
    '''
    while self.steps:
      callback, args, kwargs = self.steps.pop()
      callback(*args, **kwargs)
