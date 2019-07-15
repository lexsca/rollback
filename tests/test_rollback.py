import mock
import pytest

from rollback import Rollback


class RollbackError(Exception):
    pass


class RollbackSubclass(Rollback):
    def doRollback(self):
        super(RollbackSubclass, self).doRollback()
        raise RollbackError("test")


class TestRollback:
    def setup_method(self):
        self.mockStep = mock.Mock()

    def teardown_method(self):
        self.mockStep = None

    def test_Rollback_sets_onError_attribute(self):
        sentinel = object()
        with Rollback(onSuccess=True, onError=sentinel) as rollback:
            assert rollback.onError is sentinel

    def test_Rollback_sets_onSuccess_attribute(self):
        sentinel = object()
        with Rollback(onError=True, onSuccess=sentinel) as rollback:
            assert rollback.onSuccess is sentinel

    def test_Rollback_sets_raiseError_attribute(self):
        sentinel = object()
        with Rollback(raiseError=sentinel) as rollback:
            assert rollback.raiseError is sentinel

    def test_Rollback_doRollback_calls_in_reverse_order(self):
        idxMax = 3
        expectedCalls = reversed([mock.call(idx) for idx in range(idxMax)])
        with Rollback() as rollback:
            for idx in range(idxMax):
                rollback.addStep(self.mockStep, idx)
            rollback.doRollback()
        self.mockStep.assert_has_calls(expectedCalls)

    def test_Rollback_raises_error_by_default(self):
        with pytest.raises(RollbackError):
            with Rollback():
                raise RollbackError("test")
            raise RuntimeError("should not raise this")

    def test_Rollback_does_not_raise_error(self):
        with pytest.raises(RollbackError):
            with Rollback(raiseError=False):
                raise RuntimeError("should not raise this")
            raise RollbackError("test")

    def test_Rollback_does_rollback_onError(self):
        with Rollback(onError=True, raiseError=False) as rollback:
            rollback.addStep(self.mockStep)
            raise RollbackError("test")
        self.mockStep.assert_called_once_with()

    def test_Rollback_does_rollback_onSuccess(self):
        with Rollback(onSuccess=True) as rollback:
            rollback.addStep(self.mockStep)
        self.mockStep.assert_called_once_with()

    def test_Rollback_does_not_rollback_onError_by_default(self):
        with Rollback(raiseError=False) as rollback:
            rollback.addStep(self.mockStep)
            raise RuntimeError("should not raise this")
        self.mockStep.has_no_calls()

    def test_Rollback_does_not_rollback_onSuccess_by_default(self):
        with Rollback() as rollback:
            rollback.addStep(self.mockStep)
        self.mockStep.has_no_calls()

    def test_Rollback_clearSteps_clears_steps(self):
        with Rollback() as rollback:
            rollback.addStep(self.mockStep)
            rollback.clearSteps()
            assert rollback.steps == []

    def test_Rollback_doRollback_clears_steps(self):
        with Rollback() as rollback:
            rollback.addStep(self.mockStep)
            rollback.doRollback()
            assert rollback.steps == []

    def test_Rollback_doRollback_raises_error(self):
        with pytest.raises(RollbackError):
            with Rollback(raiseError=False) as rollback:

                def doError():
                    raise RollbackError("test")

                rollback.addStep(doError)
                rollback.doRollback()

    def test_Rollback_doRollback_raises_error_as_subclass(self):
        with pytest.raises(RollbackError):
            with RollbackSubclass(raiseError=False) as rollback:
                rollback.doRollback()

    def test_Rollback_as_standalone_instance(self):
        rollback = Rollback()
        rollback.addStep(self.mockStep)
        rollback.doRollback()
        self.mockStep.assert_called_once_with()
