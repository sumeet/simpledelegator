import cPickle as pickle
import doctest
import unittest

from expecter import expect
import mock

from simpledelegator import SimpleDelegator, get_delegated, set_delegated


class SimpleDelegatorTest(unittest.TestCase):

    def test_delegates_to_an_instance_variable(self):
        obj = mock.Mock()
        obj.instancevar = mock.Mock()
        delegator = SimpleDelegator(obj)
        expect(delegator.instancevar) == obj.instancevar

    def test_delegates_to_an_instancemethod(self):
        value = mock.Mock()
        class Obj(object):
            def instancemethod(self):
                return value
        delegator = SimpleDelegator(Obj())
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

    def test_delegates_equality(self):
        obj = mock.Mock()
        delegator = SimpleDelegator(obj)
        expect(delegator) == obj

    def test_delegates_non_equality(self):
        obj = mock.Mock()
        delegator = SimpleDelegator(mock.Mock())
        expect(delegator) != obj

    def test_delegates_iteration(self):
        delegator = SimpleDelegator(['a', 'b', 'c'])
        expect(list(iter(delegator))) == ['a', 'b', 'c']
        expect(list(enumerate(delegator))) == [(0, 'a'), (1, 'b'), (2, 'c')]

    def test_delegates_various_magic_methods(self):
        obj = mock.MagicMock()
        delegator = SimpleDelegator(obj)
        expect(str(delegator)) == str(obj)
        expect(int(delegator)) == int(obj)
        expect(len(delegator)) == len(obj)
        expect(bool(delegator)) == bool(obj)

    def test_sets_attributes_on_the_delegated_object(self):
        obj = mock.Mock()
        delegator = SimpleDelegator(obj)
        delegator.some_attr = mock.Mock()
        expect(obj.some_attr) == delegator.some_attr

    def test_can_be_pickled(self):
        obj = [1, 2, 3]
        delegator = SimpleDelegator(obj)
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

    def test_contains_tests(self):
        expect(doctest.testfile('README.markdown').attempted) > 0

    def test_does_not_fail(self):
        expect(doctest.testfile('README.markdown').failed) == 0

if __name__ == '__main__':
    unittest.main()
