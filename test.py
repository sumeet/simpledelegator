import cPickle as pickle
import unittest

from expecter import add_expectation, expect
import mock

from simpledelegator import SimpleDelegator, delegated


class EmptyDelegator(SimpleDelegator):
    pass


class SimpleDelegatorTest(unittest.TestCase):

    def test_delegates_to_an_instance_variable(self):
        obj = mock.Mock()
        obj.instancevar = mock.Mock()
        delegator = EmptyDelegator(obj)
        expect(delegator.instancevar) == obj.instancevar

    def test_delegates_to_an_instancemethod(self):
        value = mock.Mock()
        class Obj(object):
            def instancemethod(self):
                return value
        delegator = EmptyDelegator(Obj())
        expect(delegator.instancemethod()) == value

    def test_returns_a_class_variable_assigned_on_the_delegator(self):
        class C(SimpleDelegator):
            classvar = 123
        c = C(mock.Mock())
        expect(c.classvar) == 123

    def test_returns_instance_method_assigned_on_the_delegator(self):
        class C(SimpleDelegator):
            def instancemethod(self):
                return 123
        c = C(mock.Mock())
        expect(c.instancemethod()) == 123

    def test_equality_delegates(self):
        obj = mock.Mock()
        delegator = EmptyDelegator(obj)
        expect(delegator) == obj

    def test_non_equality_delegates(self):
        obj = mock.Mock()
        delegator = EmptyDelegator(mock.Mock())
        expect(delegator) != obj

    def test_iteration_delegates(self):
        obj = ['a', 'b', 'c']
        delegator = EmptyDelegator(obj)
        expect(list(enumerate(delegator))) == [(0, 'a'), (1, 'b'), (2, 'c')]

    def test_delegates_various_magic_methods(self):
        obj = mock.MagicMock()
        delegator = EmptyDelegator(obj)
        expect(str(delegator)) == str(obj)
        expect(int(delegator)) == int(obj)
        expect(iter(delegator)) == iter(obj)
        expect(len(delegator)) == len(obj)
        expect(bool(delegator)) == bool(obj)

    def test_attributes_are_set_on_the_delegated_object(self):
        obj = mock.Mock()
        delegator = EmptyDelegator(obj)
        delegator.some_attr = mock.Mock()
        expect(obj.some_attr) == delegator.some_attr

    def test_can_be_pickled(self):
        delegator = EmptyDelegator([1, 2, 3])
        pickled = pickle.dumps(delegator)
        del delegator
        unpickled_delegator = pickle.loads(pickled)
        # XXX: There should be a less arbitrary way to verify the correctness
        # of the unpickled delegator.
        expect(list(reversed(unpickled_delegator))) == [3, 2, 1]

    def test_can_read_from_properties(self):
        class C(SimpleDelegator):
            @property
            def prop(self):
                return 123
        c = C(mock.Mock())
        expect(c.prop) == 123

    def test_can_override_setters(self):
        container = mock.Mock()
        class C(SimpleDelegator):
            @property
            def prop(self):
                return container.value

            @prop.setter
            def prop(self, value):
                container.value = value

        value = mock.Mock()
        c = C(mock.Mock())
        c.prop = value
        expect(c.prop) == value


class DelegatedTest(unittest.TestCase):

    def test_returns_object_inside_simple_delegator(self):
        obj = mock.Mock()
        delegator = SimpleDelegator(obj)
        expect(delegated(delegator)) == obj


if __name__ == '__main__':
    unittest.main()
