# compilerdesign

A Python library for demonstrating core **Compiler Design** concepts. Import it as `cd` and use clean, simple functions covering everything from lexical analysis to intermediate code generation.

```bash
pip install compilerdesign
```

---

## Quick Start

```python
import compilerdesign as cd
```

---

## Features & API Reference

### 1. Lexical Analyzer

```python
code = """
int main() {
    int x = 10;
    float y = 3.14;
    return x + y;
}
"""
result = cd.lexical_analyzer(code)
print(result['summary'])
# {'total_tokens': 24, 'keywords': 5, 'identifiers': 4, 'integer_constants': 1,
#  'float_constants': 1, 'operators': 3, ...}
print(result['tokens'])       # list of (token_type, value)
print(result['unique_identifiers'])  # ['main', 'x', 'y']
```

---

### 2. Grammar Transformations

Grammar format: `dict` mapping non-terminal → list of production strings.

```python
grammar = {
    'E': ['E + T', 'T'],
    'T': ['T * F', 'F'],
    'F': ['( E )', 'id']
}

# Eliminate Left Recursion
new_g = cd.eliminate_left_recursion(grammar)
# {'E': ["T E'"], "E'": ["+ T E'", 'ε'], 'T': ["F T'"], "T'": ["* F T'", 'ε'], ...}

# Left Factoring
grammar2 = {'A': ['a b', 'a c', 'd']}
factored = cd.left_factoring(grammar2)
# {'A': ["a A'", 'd'], "A'": ['b', 'c']}

# Check Ambiguity
result = cd.check_ambiguity(grammar)
# {'ambiguous': False, 'issues': []}
```

---

### 3. FIRST and FOLLOW Sets

```python
grammar = {
    'E':  ['T R'],
    'R':  ['+ T R', 'ε'],
    'T':  ['F Y'],
    'Y':  ['* F Y', 'ε'],
    'F':  ['( E )', 'i']
}

result = cd.compute_first_follow(grammar, start='E')
print(result['FIRST'])   # {'E': ['(', 'i'], 'R': ['+', 'ε'], ...}
print(result['FOLLOW'])  # {'E': ['$', ')'], 'R': ['$', ')'], ...}

# Or individually:
first  = cd.compute_first(grammar)
follow = cd.compute_follow(grammar, start='E')
```

---

### 4. LL(1) Predictive Parsing Table

```python
table_result = cd.build_ll1_table(grammar, start='E')
print(table_result['is_ll1'])     # True/False
print(table_result['table'])      # {(NonTerminal, Terminal): production}
print(table_result['conflicts'])  # list of conflict strings

# Parse a token string
parse = cd.ll1_parse(grammar, tokens=['i', '+', 'i', '*', 'i'], start='E')
print(parse['accepted'])  # True
for step in parse['steps']:
    print(step)
```

---

### 5. Shift-Reduce Parsing

```python
productions = [
    ('E', ['E', '+', 'T']),
    ('E', ['T']),
    ('T', ['T', '*', 'F']),
    ('T', ['F']),
    ('F', ['id'])
]
result = cd.shift_reduce_parse(productions, tokens=['id', '+', 'id'])
print(result['accepted'])  # True
for step in result['steps']:
    print(step)  # {'stack': [...], 'input': [...], 'action': '...'}
```

---

### 6. LEADING and TRAILING Sets

```python
result = cd.compute_leading_trailing(grammar)
print(result['LEADING'])   # {'E': ['(', '+', '*', 'i'], ...}
print(result['TRAILING'])  # {'E': [')', '+', '*', 'i'], ...}
```

---

### 7. LR(0) Items

```python
productions = [
    ('E', ['E', '+', 'T']),
    ('E', ['T']),
    ('T', ['id'])
]
result = cd.compute_lr0_items(productions, start='E')
print(f"Total states: {result['num_states']}")
for state in result['states']:
    print(f"\nState {state['id']}:")
    for item in state['items']:
        print(f"  {item}")
for (frm, sym, to) in result['transitions']:
    print(f"  State {frm} --{sym}--> State {to}")
```

---

### 8. Intermediate Code Generation

```python
# Infix → Postfix (RPN)
cd.infix_to_postfix("a + b * c")      # "a b c * +"
cd.infix_to_postfix("(a + b) * c")    # "a b + c *"

# Infix → Prefix (Polish Notation)
cd.infix_to_prefix("a + b * c")       # "+ a * b c"

# Postfix → Infix
cd.postfix_to_infix("a b c * +")      # "(a + (b * c))"

# Prefix → Infix
cd.prefix_to_infix("+ a * b c")       # "(a + (b * c))"

# Universal converter
cd.convert_expression("a + b * c", from_notation="infix", to_notation="postfix")
cd.convert_expression("a b c * +",  from_notation="postfix", to_notation="prefix")
```

---

## Publishing to PyPI

See [PUBLISHING.md](PUBLISHING.md) for step-by-step instructions.

---

## License

MIT
