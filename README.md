# Y-Combinator
Python implementation of chapters 9, 10 of Daniel Friedman's "Little Schemer"

# But Y
Chapter 9 described how to construct the Y Combinator, which in Python looks pretty nice:

```python
Y = lambda le: (lambda f: f(f))(lambda f: le( lambda x: f(f)(x)))
```
Chapter 10 includes a smol Lisp interpreter, which fully support the Y combinator, albeit in unparsed abstract-syntax-tree form for now:
```python
Y = ['lambda', ['le'], [['lambda', ['f'],['f','f']],['lambda', ['f'], ['le', ['lambda', ['x'], [['f', 'f'], 'x']]]]]]
```

# TODO
1. Parser to turn normal Lisp into the AST 
2. Compare this minimal Lisp implementation to the one described in http://www.paulgraham.com/rootsoflisp.html
