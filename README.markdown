# SimpleDelegator

A clone of Ruby's [SimpleDelegator] [1]. This was mostly an experiment to see
if Python could pull this off.

Here's an example using SimpleDelegator as an object decorator.

```python
>>> from simpledelegator import SimpleDelegator, get_delegated
>>> from collections import namedtuple
>>> class NotADuck(SimpleDelegator):
        def quack(self):
            my_type = type(get_delegated(self)).__name__
            print 'i am not a duck but i am a %s!' % my_type
>>> Cow = namedtuple('Cow', 'weight')
>>> cow = Cow(weight='heavy')
>>> animal = NotADuck(cow)
>>> animal.quack()
i am not a duck but i am a Cow!
>>> animal.weight
'heavy'
```

[1]: http://ruby-doc.org/stdlib-1.9.3/libdoc/delegate/rdoc/SimpleDelegator.html
