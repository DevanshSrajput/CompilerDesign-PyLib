# compilerdesign

A teaching Python library that covers the **entire Compiler Design
syllabus** in one `import`. Every function returns a plain dict / str,
and every function has a matching `show_*` pretty-printer so you can
read the output at a glance.

```bash
pip install compilerdesign
```

```python
import compilerdesign as cd

cd.show_lexical(cd.lexical_analyzer("int x = 10;"))
```

> Full walkthrough with input formats, outputs and end-to-end examples
> lives in **[DOCUMENTATION.md](DOCUMENTATION.md)**.
> Version history: **[CHANGES.md](CHANGES.md)**.

---

## What's inside

| Topic                              | Core function                     | Pretty-printer                |
|------------------------------------|-----------------------------------|-------------------------------|
| Lexical analysis                   | `lexical_analyzer`                | `show_lexical`                |
| Symbol table                       | `build_symbol_table`              | `show_symbol_table`           |
| Left-recursion elimination         | `eliminate_left_recursion`        | `show_grammar`                |
| Left factoring                     | `left_factoring`                  | `show_grammar`                |
| Ambiguity check (heuristic)        | `check_ambiguity`                 | `show_ambiguity`              |
| FIRST / FOLLOW                     | `compute_first_follow`            | `show_first_follow`           |
| LEADING / TRAILING                 | `compute_leading_trailing`        | `show_leading_trailing`       |
| LL(1) table + parse trace          | `build_ll1_table` / `ll1_parse`   | `show_ll1_table` / `show_parse_trace` |
| Shift-reduce parser                | `shift_reduce_parse`              | `show_parse_trace`            |
| LR(0) canonical collection         | `compute_lr0_items`               | `show_lr0`                    |
| Infix ↔ Postfix ↔ Prefix           | `convert_expression`, etc.        | `show_expression`             |
| Three-address code (quadruples)    | `generate_three_address_code`     | `show_three_address_code`     |
| DAG of an expression               | `build_dag`                       | `show_dag`                    |

---

## 60-second tour

```python
import compilerdesign as cd

# 1) Lexical + Symbol table
src = """
int add(int a, int b) {
    int c = a + b * 2;
    return c;
}
"""
cd.show_lexical(cd.lexical_analyzer(src))
cd.show_symbol_table(cd.build_symbol_table(src))

# 2) Expression → 3AC → DAG
expr = "a + b * c - d"
cd.show_three_address_code(cd.generate_three_address_code(expr))
cd.show_dag(cd.build_dag(expr))

# 3) Grammar pipeline
g = {'E': ['E + T', 'T'], 'T': ['T * F', 'F'], 'F': ['( E )', 'id']}
g = cd.eliminate_left_recursion(g)
cd.show_grammar(g, "NO LEFT RECURSION")
cd.show_first_follow(cd.compute_first_follow(g, start='E'))
cd.show_ll1_table(cd.build_ll1_table(g, start='E'))
cd.show_parse_trace(
    cd.ll1_parse(g, ['id', '+', 'id', '*', 'id'], start='E'),
    "LL(1) PARSE",
)
```

---

## Grammar input format

```python
grammar = {
    'E': ['E + T', 'T'],    # each production is a space-separated string
    'T': ['T * F', 'F'],
    'F': ['( E )', 'id'],
}
# epsilon: 'ε' or 'eps'
```

Shift-reduce / LR(0) take a list of tuples instead:

```python
productions = [
    ('E', ['E', '+', 'T']),
    ('E', ['T']),
    ('T', ['id']),
]
```

---

## Running tests

```bash
python test_all.py
```

---

## License

MIT — see [DOCUMENTATION.md](DOCUMENTATION.md) for the full reference.
