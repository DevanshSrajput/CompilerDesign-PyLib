"""
Grammar transformations: eliminate left recursion and perform left factoring.

Grammar format:
    A dict mapping non-terminal (str) -> list of productions (list of str).
    Each production is a space-separated string of symbols.
    Use 'eps' or 'ε' to represent epsilon.

Example:
    grammar = {
        'E': ['E + T', 'T'],
        'T': ['T * F', 'F'],
        'F': ['( E )', 'id']
    }
"""

EPSILON = 'ε'


def _normalize(prod: str) -> str:
    return prod.strip().replace('eps', EPSILON)


def eliminate_left_recursion(grammar: dict) -> dict:
    """
    Eliminate immediate left recursion from each production.
    Handles A -> A alpha | beta patterns.

    Returns a new grammar dict with left recursion eliminated.
    """
    new_grammar = {}
    for A, productions in grammar.items():
        alpha = []  # recursive: starts with A
        beta = []   # non-recursive

        for prod in productions:
            symbols = _normalize(prod).split()
            if symbols[0] == A:
                alpha.append(' '.join(symbols[1:]))  # strip leading A
            else:
                beta.append(' '.join(symbols))

        if not alpha:
            # No left recursion for this non-terminal
            new_grammar[A] = [_normalize(p) for p in productions]
        else:
            A_prime = A + "'"
            # A  -> beta A'
            new_grammar[A] = [b + ' ' + A_prime for b in beta] if beta else [A_prime]
            # A' -> alpha A' | ε
            new_grammar[A_prime] = [a + ' ' + A_prime for a in alpha] + [EPSILON]

    return new_grammar


def left_factoring(grammar: dict) -> dict:
    """
    Apply left factoring to eliminate common prefixes in productions.

    Returns a new grammar dict after left factoring.
    """
    new_grammar = {}
    counter = {}

    def _factor(A, productions):
        if len(productions) <= 1:
            new_grammar[A] = [_normalize(p) for p in productions]
            return

        # Group by first symbol
        groups = {}
        for prod in productions:
            symbols = _normalize(prod).split()
            first = symbols[0] if symbols else EPSILON
            groups.setdefault(first, []).append(symbols)

        new_prods = []
        for prefix, group in groups.items():
            if len(group) == 1:
                new_prods.append(' '.join(group[0]))
            else:
                # Find longest common prefix
                lcp = group[0]
                for g in group[1:]:
                    lcp = _common_prefix(lcp, g)

                counter[A] = counter.get(A, 0) + 1
                A_prime = A + "'" * counter[A]
                new_prods.append(' '.join(lcp) + ' ' + A_prime)

                # Remainders after removing the common prefix
                remainders = []
                for g in group:
                    rest = g[len(lcp):]
                    remainders.append(' '.join(rest) if rest else EPSILON)

                _factor(A_prime, remainders)

        new_grammar[A] = new_prods

    def _common_prefix(a, b):
        prefix = []
        for x, y in zip(a, b):
            if x == y:
                prefix.append(x)
            else:
                break
        return prefix

    for A, productions in grammar.items():
        _factor(A, productions)

    return new_grammar


def check_ambiguity(grammar: dict) -> dict:
    """
    Basic ambiguity check: detects if any non-terminal has duplicate productions
    or productions with the same first symbol (a heuristic, not complete detection).

    Returns {'ambiguous': bool, 'issues': list of str}
    """
    issues = []
    for A, prods in grammar.items():
        norm = [_normalize(p) for p in prods]
        if len(norm) != len(set(norm)):
            issues.append(f"{A} has duplicate productions.")
        first_symbols = [p.split()[0] if p.split() else EPSILON for p in norm]
        if len(first_symbols) != len(set(first_symbols)):
            issues.append(f"{A} has productions with the same leading symbol (possible ambiguity).")

    return {
        'ambiguous': len(issues) > 0,
        'issues': issues
    }
