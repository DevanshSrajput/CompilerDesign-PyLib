"""Tests for the compilerdesign library."""
import io
import sys
from contextlib import redirect_stdout

sys.path.insert(0, '.')

import compilerdesign as cd


def test_help():
    message = cd.help()
    assert "compilerdesign v1.1.0" in message
    assert "Aditya" in message
    assert "aditya-ig10" in message
    print("OK help")


def test_lexical():
    code = "int main() { int x = 10; return x + 1; }"
    r = cd.lexical_analyzer(code)
    assert r['summary']['keywords'] >= 2
    assert 'x' in r['unique_identifiers']
    print("OK lexical_analyzer")


def test_left_recursion():
    grammar = {'E': ['E + T', 'T'], 'T': ['T * F', 'F'], 'F': ['( E )', 'id']}
    new_g = cd.eliminate_left_recursion(grammar)
    assert "E'" in new_g
    assert "T'" in new_g
    print("OK eliminate_left_recursion")


def test_left_factoring():
    grammar = {'A': ['a b', 'a c', 'd']}
    new_g = cd.left_factoring(grammar)
    assert "A'" in new_g
    print("OK left_factoring")


def test_ambiguity():
    grammar = {'A': ['a', 'a']}
    r = cd.check_ambiguity(grammar)
    assert r['ambiguous'] is True
    print("OK check_ambiguity")


def test_first_follow():
    grammar = {
        'E':  ['T R'], 'R':  ['+ T R', 'ε'],
        'T':  ['F Y'], 'Y':  ['* F Y', 'ε'],
        'F':  ['( E )', 'i']
    }
    r = cd.compute_first_follow(grammar, start='E')
    assert '(' in r['FIRST']['E']
    assert '$' in r['FOLLOW']['E']
    print("OK compute_first_follow")


def test_ll1_table():
    grammar = {
        'E':  ['T R'], 'R':  ['+ T R', 'ε'],
        'T':  ['F Y'], 'Y':  ['* F Y', 'ε'],
        'F':  ['( E )', 'i']
    }
    r = cd.build_ll1_table(grammar, start='E')
    assert r['is_ll1'] is True
    print("OK build_ll1_table")


def test_ll1_parse():
    grammar = {
        'E':  ['T R'], 'R':  ['+ T R', 'ε'],
        'T':  ['F Y'], 'Y':  ['* F Y', 'ε'],
        'F':  ['( E )', 'i']
    }
    r = cd.ll1_parse(grammar, ['i', '+', 'i'], start='E')
    assert r['accepted'] is True
    print("OK ll1_parse")


def test_shift_reduce():
    productions = [('E', ['E', '+', 'T']), ('E', ['T']), ('T', ['id'])]
    r = cd.shift_reduce_parse(productions, ['id', '+', 'id'])
    assert r['accepted'] is True
    print("OK shift_reduce_parse")


def test_leading_trailing():
    grammar = {
        'E':  ['T R'], 'R':  ['+ T R', 'ε'],
        'T':  ['F Y'], 'Y':  ['* F Y', 'ε'],
        'F':  ['( E )', 'i']
    }
    r = cd.compute_leading_trailing(grammar)
    assert 'i' in r['LEADING']['E']
    print("OK compute_leading_trailing")


def test_lr0():
    productions = [('E', ['E', '+', 'T']), ('E', ['T']), ('T', ['id'])]
    r = cd.compute_lr0_items(productions, start='E')
    assert r['num_states'] > 0
    print("OK compute_lr0_items")


def test_intermediate_code():
    assert cd.infix_to_postfix("a + b * c") == "a b c * +"
    assert cd.infix_to_prefix("a + b * c") == "+ a * b c"
    assert cd.postfix_to_infix("a b c * +") == "(a + (b * c))"
    assert cd.prefix_to_infix("+ a * b c") == "(a + (b * c))"
    assert cd.convert_expression("a + b * c", "infix", "postfix") == "a b c * +"
    print("OK intermediate_code (all conversions)")


def test_symbol_table():
    code = """
    int globalVar;
    int add(int a, int b) {
        int sum = a + b;
        return sum;
    }
    """
    r = cd.build_symbol_table(code)
    names = [e["name"] for e in r["entries"]]
    assert "add" in names
    assert "a" in names and "b" in names
    assert "sum" in names
    assert r["total"] == len(r["entries"])
    print("OK build_symbol_table")


def test_three_address_code():
    r = cd.generate_three_address_code("a + b * c")
    assert len(r["quadruples"]) == 2
    assert r["final"] == "t2"
    assert r["pretty"] == ["t1 = b * c", "t2 = a + t1"]
    print("OK generate_three_address_code")


def test_dag():
    r = cd.build_dag("a + a * b")
    labels = [n["label"] for n in r["nodes"]]
    # 'a' must appear only once (shared sub-expression)
    assert labels.count("a") == 1
    assert r["root"] == len(r["nodes"]) - 1
    print("OK build_dag")


def test_all_show_functions_run():
    """Every pretty-printer should run without raising."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = "int x = 10; int y = x + 1;"
        cd.show_lexical(cd.lexical_analyzer(code))
        cd.show_symbol_table(cd.build_symbol_table(code))
        g = {'E': ['E + T', 'T'], 'T': ['T * F', 'F'], 'F': ['( E )', 'id']}
        cd.show_grammar(g, "GRAMMAR")
        cd.show_grammar(cd.eliminate_left_recursion(g), "NO LR")
        cd.show_ambiguity(cd.check_ambiguity({'A': ['a', 'a']}))
        g2 = {
            'E':  ['T R'], 'R':  ['+ T R', 'ε'],
            'T':  ['F Y'], 'Y':  ['* F Y', 'ε'],
            'F':  ['( E )', 'i']
        }
        cd.show_first_follow(cd.compute_first_follow(g2, start='E'))
        cd.show_leading_trailing(cd.compute_leading_trailing(g2))
        cd.show_ll1_table(cd.build_ll1_table(g2, start='E'))
        cd.show_parse_trace(cd.ll1_parse(g2, ['i', '+', 'i'], start='E'))
        prods = [('E', ['E', '+', 'T']), ('E', ['T']), ('T', ['id'])]
        cd.show_parse_trace(cd.shift_reduce_parse(prods, ['id', '+', 'id']))
        cd.show_lr0(cd.compute_lr0_items(prods, start='E'))
        cd.show_three_address_code(cd.generate_three_address_code("a + b * c"))
        cd.show_dag(cd.build_dag("a + b * c"))
    assert "LEXICAL ANALYSIS" in buf.getvalue()
    assert "SYMBOL TABLE" in buf.getvalue()
    assert "THREE-ADDRESS CODE" in buf.getvalue()
    assert "DAG" in buf.getvalue()
    print("OK all show_* pretty-printers run")


if __name__ == "__main__":
    print("Running compilerdesign tests...\n")
    test_help()
    test_lexical()
    test_left_recursion()
    test_left_factoring()
    test_ambiguity()
    test_first_follow()
    test_ll1_table()
    test_ll1_parse()
    test_shift_reduce()
    test_leading_trailing()
    test_lr0()
    test_intermediate_code()
    test_symbol_table()
    test_three_address_code()
    test_dag()
    test_all_show_functions_run()
    print("\nAll tests passed!")
