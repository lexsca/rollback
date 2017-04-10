Rollback
========

Simple mechanism for rolling back multiple operations in a predictable way,
either as a context manager or a standalone instance. By default, errors are
re-raised, but an explicit mode or call *must* be supplied to trigger a
rollback.  Valid modes are:

* `onError`  Boolean when `True` will roll back if an error is raised
* `onSuccess` Boolean when `True` will roll back if an error is _not_ raised

Both modes can be set to `True` to always rollback. A rollback can also be
triggered manually by calling `doRollback`. Errors can be supressed by
setting `raiseError` to `False`.  

## Installation

    python setup.py install

## Example usage

```python
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
```
