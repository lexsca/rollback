Rollback
========

This is a simple Pythonic mechanism for rolling back multiple operations in a predictable way, usable as a `context manager`_ or a standalone instance (see `Example usage`_). By default, errors are re-raised, but an explicit mode or call *must* be supplied to trigger a rollback. Valid modes are:

-  ``onError`` Boolean when ``True`` will roll back if an error is
   raised
-  ``onSuccess`` Boolean when ``True`` will roll back if an error is
   *not* raised

Both modes can be set to ``True`` to always rollback. A rollback can also be triggered manually by calling ``doRollback``.  Note that multiple calls to ``doRollback`` will only call the rollback steps once.

Errors can be supressed by setting ``raiseError`` to ``False``. Note that errors from rollback steps will not be surpressed, regardless of the ``raiseError`` setting.

If a rollback is triggered, each step is called in a last in, first out order (LIFO). That is, the most recently added step is called first, the first step is called last.

Compatibility
~~~~~~~~~~~~~

Rollback was tested with the following versions of Python:

-  3.7.4
-  3.6.9
-  3.5.7
-  3.4.10
-  3.3.7
-  2.7.16
-  2.6.9

Installation
~~~~~~~~~~~~

Install from source:

::

  python setup.py install

Install from PyPI:

::

  pip install rollback

Example usage
~~~~~~~~~~~~~

.. code:: python

  from __future__ import print_function

  from rollback import Rollback

  # *always* rollback after exiting block, letting any error be re-raised
  with Rollback(onError=True, onSuccess=True) as rollback:
    print('do a1')
    rollback.addStep(print, 'undo a1')
    print('do a2')
    rollback.addStep(print, 'undo a2')

  # rollback *only* if *no* error is raised, letting any error be re-raised
  with Rollback(onSuccess=True) as rollback:
    print('do b1')
    rollback.addStep(print, 'undo b1')
    print('do b2')
    rollback.addStep(print, 'undo b2')

  # rollback manually
  with Rollback() as rollback:
    print('do c1')
    rollback.addStep(print, 'undo c1')
    print('do c2')
    rollback.addStep(print, 'undo c2')
    rollback.doRollback()

  # rollback *only* if an error is raised, suppressing the error
  with Rollback(onError=True, raiseError=False) as rollback:
    print('do d1')
    rollback.addStep(print, 'undo d1')
    print('do d2')
    rollback.addStep(print, 'undo d2')
    raise RuntimeError('this is not re-raised')

  # rollback *only* if an error is raised, letting the error be re-raised
  with Rollback(onError=True) as rollback:
    print('do e1')
    rollback.addStep(print, 'undo e1')
    print('do e2')
    rollback.addStep(print, 'undo e2')
    raise RuntimeError('this is re-raised')

Produces output:

::

  do a1
  do a2
  undo a2
  undo a1
  do b1
  do b2
  undo b2
  undo b1
  do c1
  do c2
  undo c2
  undo c1
  do d1
  do d2
  undo d2
  undo d1
  do e1
  do e2
  undo e2
  undo e1
  Traceback (most recent call last):
    File "example.py", line 41, in <module>
      raise RuntimeError('this is re-raised')
  RuntimeError: this is re-raised

.. _context manager: https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers
