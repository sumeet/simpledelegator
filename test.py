import cPickle as pickle
import doctest
import unittest

from expecter import expect
import mock

from simpledelegator import SimpleDelegator, get_delegated, set_delegated


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
        obj = [1, 2, 3]
        delegator = EmptyDelegator(obj)
        pickled = pickle.dumps(delegator)
        del delegator
        unpickled_delegator = pickle.loads(pickled)
        expect(get_delegated(unpickled_delegator)) == obj

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


class GetDelegatedTest(unittest.TestCase):

    def test_returns_object_inside_delegator(self):
        obj = mock.Mock()
        delegator = SimpleDelegator(obj)

        expect(get_delegated(delegator)) == obj


class SetDelegatedTest(unittest.TestCase):

    def test_sets_object_inside_delegator(self):
        delegator = SimpleDelegator(mock.Mock())
        another_obj = mock.Mock()
        set_delegated(delegator, another_obj)

        expect(get_delegated(delegator)) == another_obj


class ReadmeTest(unittest.TestCase):

    def test_example_in_readme_exists(self):
        expect(doctest.testfile('README.markdown').attempted) > 0

    def test_example_in_readme_does_not_fail(self):
        expect(doctest.testfile('README.markdown').failed) == 0

if __name__ == '__main__':
    unittest.main()
