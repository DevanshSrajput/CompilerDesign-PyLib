"""
Computation of LEADING and TRAILING sets for operator precedence parsing.

Grammar format: same dict format as other modules.
LEADING(A)  = set of terminals that can appear as the leftmost terminal in a derivation of A.
TRAILING(A) = set of terminals that can appear as the rightmost terminal in a derivation of A.
"""

EPSILON = 'ε'


def compute_leading(grammar: dict) -> dict:
    """
    Compute LEADING sets for all non-terminals.
    LEADING(A): terminals t such that A =>* t... or A =>* B t...
    """
    leading = {nt: set() for nt in grammar}
    changed = True

    while changed:
        changed = False
        for A, productions in grammar.items():
            for prod in productions:
                symbols = prod.strip().split()
                if not symbols or symbols == [EPSILON]:
                    continue

                i = 0
                while i < len(symbols):
                    sym = symbols[i]
                    if sym not in grammar:
                        # Terminal
                        before = len(leading[A])
                        leading[A].add(sym)
                        if len(leading[A]) > before:
                            changed = True
                        break
                    else:
                        # Non-terminal: add its LEADING set
                        before = len(leading[A])
                        leading[A].update(leading[sym])
                        if len(leading[A]) > before:
                            changed = True
                        # Check if the next symbol after non-terminal should also be explored
                        # Only if the non-terminal can derive ε (simplified: check if ε prod exists)
                        if any(p.strip() == EPSILON for p in grammar[sym]):
                            i += 1
                        else:
                            break

    return {k: sorted(v) for k, v in leading.items()}


def compute_trailing(grammar: dict) -> dict:
    """
    Compute TRAILING sets for all non-terminals.
    TRAILING(A): terminals t such that A =>* ...t or A =>* ...t B
    """
    trailing = {nt: set() for nt in grammar}
    changed = True

    while changed:
        changed = False
        for A, productions in grammar.items():
            for prod in productions:
                symbols = prod.strip().split()
                if not symbols or symbols == [EPSILON]:
                    continue

                i = len(symbols) - 1
                while i >= 0:
                    sym = symbols[i]
                    if sym not in grammar:
                        before = len(trailing[A])
                        trailing[A].add(sym)
                        if len(trailing[A]) > before:
                            changed = True
                        break
                    else:
                        before = len(trailing[A])
                        trailing[A].update(trailing[sym])
                        if len(trailing[A]) > before:
                            changed = True
                        if any(p.strip() == EPSILON for p in grammar[sym]):
                            i -= 1
                        else:
                            break

    return {k: sorted(v) for k, v in trailing.items()}


def compute_leading_trailing(grammar: dict) -> dict:
    """
    Convenience: returns both LEADING and TRAILING sets.
    """
    return {
        'LEADING': compute_leading(grammar),
        'TRAILING': compute_trailing(grammar)
    }
