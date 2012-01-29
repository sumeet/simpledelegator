# SimpleDelegator

A clone of Ruby's [SimpleDelegator] [1]. This was mostly an experiment to see
if Python could pull this off.

Here's an example using SimpleDelegator as an object decorator.

```python
    >>> from simpledelegator import SimpleDelegator, get_delegated
    >>> from collections import namedtuple

    >>> User = namedtuple('User', 'first_name last_name')
    >>> class UserPresenter(SimpleDelegator):
    ...     @property
    ...     def name(self):
    ...         return self.first_name + ' ' + self.last_name

    >>> user = UserPresenter(User('Bob', 'Smith'))
    >>> user.first_name
    'Bob'
    >>> user.last_name
    'Smith'
    >>> user.name
    'Bob Smith'

```

[1]: http://ruby-doc.org/stdlib-1.9.3/libdoc/delegate/rdoc/SimpleDelegator.html
