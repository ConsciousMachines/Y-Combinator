error = lambda x: print(x)


def lookup_in_entry_help(name, names, values, entry_f):
    if names == []:
        return entry_f(name)
    if names[0] == name:
        return values[0]
    return lookup_in_entry_help(name, names[1:], values[1:], entry_f)

build = lambda a, b: [a, b]

lookup_in_entry = lambda name, entry, entry_f: lookup_in_entry_help(name, entry[0], entry[1], entry_f)

extend_table = lambda a, b: [a] + b

lookup_in_table = lambda name, table, table_f: table_f(name) if table == [] else lookup_in_entry(name, table[0], lambda name: (lookup_in_table(name, table[1:], table_f)))



def evlis(args, table):
    if args == []:
        return []
    return [meaning(args[0], table)] + evlis(args[1:], table)


def _atom(x):
    if type(x) == str: return True 
    if x == []: return False 
    if x[0] == 'primitive': return True 
    if x[0] == 'non-primitive': return True 
    return False 


apply_closure = lambda closure, vals: meaning(closure[2], 
    extend_table(build(closure[1], vals),closure[0]))


def apply_primitive(name, vals):
    if name == 'cons': 
        return [vals[0]] + vals[1]
    if name == 'car': 
        return vals[0][0]
    if name == 'cdr': 
        return vals[0][1:]
    if name == 'null?': 
        return vals[0] == []
    if name == 'eq?':
        return vals[0] == vals[1]
    if name == 'atom?':
        return _atom(vals[0])
    if name == 'zero?':
        return int(vals[0]) == 0
    if name == 'add1':
        return int(vals[0]) + 1
    if name == 'sub1':
        return int(vals[0]) - 1
    if name == 'number?':
        return vals[0].isnumeric()


apply = lambda fun, vals: apply_primitive(fun[1], vals) if fun[0] == 'primitive' else apply_closure(fun[1], vals)

_application = lambda e, table: apply(meaning(e[0], table), evlis(e[1:], table))

_quote = lambda e, table: e[1]

_identifier = lambda e, table: lookup_in_table(e, table, error)

_lambda = lambda e, table: build('non-primitive', [table] + e[1:])


def _const(e, table):
    if e.isnumeric(): return e 
    if e == '#t': return True 
    if e == '#f': return False
    return build('primitive', e)


def evcon(lines, table):
    if lines[0][0] == 'else':
        return meaning(lines[0][1], table)
    if meaning(lines[0][0], table):
        return meaning(lines[0][1], table)
    return evcon(lines[1:], table)


_cond = lambda e, table: evcon(e[1:], table) 


def atom_to_action(e):
    if e.isnumeric(): return _const
    if e == '#t': return _const
    if e == '#f': return _const
    if e == 'cons': return _const
    if e == 'car': return _const
    if e == 'cdr': return _const
    if e == 'null?': return _const
    if e == 'eq?': return _const
    if e == 'atom?': return _const
    if e == 'zero?': return _const
    if e == 'add1': return _const
    if e == 'sub1': return _const
    if e == 'number?': return _const
    return _identifier


def list_to_action(e):
    if type(e[0]) == str: # the non-application means its not fully evaluated!
        if e[0] == 'quote': return _quote 
        if e[0] == 'lambda': return _lambda 
        if e[0] == 'cond': return _cond
        return _application
    return _application


expression_to_action = lambda e: atom_to_action(e) if type(e) == str else list_to_action(e)

meaning = lambda e, table: expression_to_action(e) (e, table)

value = lambda e: meaning(e, []) # invokes meaning on expression with an empty table





Y = ['lambda', ['le'], [['lambda', ['f'],['f','f']],['lambda', ['f'], ['le', ['lambda', ['x'], [['f', 'f'], 'x']]]]]]

lenfac = ['lambda', ['mk_length'], ['lambda', ['l'], ['cond', [['null?', 'l'],'0'],['else', ['add1', ['mk_length', ['cdr','l']]]]]]]

length = ['lambda', ['l'], ['cond', [['null?', 'l'], '0'], ['else', '1']]]

value([length, ['quote', [1,2]]])
value([[lenfac, length], ['quote', [1,2, 3]]])
value([[Y, lenfac], ['quote', ['1', '2', '3']]])

[lambda, [le], [rep,fac]]
[lambda, [le], [[lambda, [f],[f,f]],[lambda, [f], [le, [lambda, [x], [[f, f], x]]]]]]

rep = lambda f: f(f)
fac = lambda f: le( lambda x: f(f)(x))






# in actual Python 
Y = lambda le: (lambda f: f(f))(lambda f: le( lambda x: f(f)(x)))

Y = lambda le: (lambda f: f(f))(lambda f: le (lambda x: f(f)(x)))


# factorial factory
fac = lambda n: 1 if n == 1 else n*fac(n-1)
facfac = lambda f: (lambda n: 1 if n == 1 else n*f(n-1))
lengthfac = (lambda length : (lambda l : 0 if l == [] else 1 + length(l[1:])))

Y(facfac)(5)
Y(lengthfac)([1,2,3,4])