"""
LR(0) Item Set Construction (Canonical Collection).

Grammar format: list of (lhs, rhs) tuples where rhs is a list of symbols.
An augmented production S' -> S is added automatically.

LR(0) Item: (lhs, rhs_before_dot, rhs_after_dot)
Represented as (lhs, tuple(before), tuple(after))
"""


def _augment(productions: list, start: str) -> tuple:
    """Add augmented production S' -> S."""
    aug_start = start + "'"
    aug_prod = [(aug_start, [start])] + list(productions)
    return aug_prod, aug_start


def _closure(items: frozenset, productions: list) -> frozenset:
    """Compute closure of a set of LR(0) items."""
    closure = set(items)
    changed = True
    while changed:
        changed = False
        for (lhs, before, after) in list(closure):
            if not after:
                continue
            next_sym = after[0]
            for (plhs, prhs) in productions:
                if plhs == next_sym:
                    new_item = (plhs, (), tuple(prhs))
                    if new_item not in closure:
                        closure.add(new_item)
                        changed = True
    return frozenset(closure)


def _goto(items: frozenset, symbol: str, productions: list) -> frozenset:
    """Compute GOTO(items, symbol)."""
    moved = set()
    for (lhs, before, after) in items:
        if after and after[0] == symbol:
            moved.add((lhs, before + (after[0],), after[1:]))
    return _closure(frozenset(moved), productions)


def compute_lr0_items(productions: list, start: str) -> dict:
    """
    Compute the canonical collection of LR(0) item sets.

    productions: list of (lhs, rhs_list) tuples
    start: start symbol string

    Returns:
        {
          'states': list of sets of item strings,
          'transitions': list of (from_state_idx, symbol, to_state_idx),
          'start_state': 0,
          'augmented_start': str
        }
    """
    aug_prods, aug_start = _augment(productions, start)

    # Initial item: S' -> . S
    initial_item = (aug_start, (), tuple([start]))
    I0 = _closure(frozenset([initial_item]), aug_prods)

    states = [I0]
    state_map = {I0: 0}
    transitions = []
    queue = [I0]

    while queue:
        current = queue.pop(0)
        current_idx = state_map[current]

        # Gather all symbols that appear after a dot
        symbols = set()
        for (lhs, before, after) in current:
            if after:
                symbols.add(after[0])

        for sym in symbols:
            goto = _goto(current, sym, aug_prods)
            if not goto:
                continue
            if goto not in state_map:
                state_map[goto] = len(states)
                states.append(goto)
                queue.append(goto)
            transitions.append((current_idx, sym, state_map[goto]))

    def fmt_item(item):
        lhs, before, after = item
        return f"{lhs} -> {' '.join(before)} . {' '.join(after)}"

    return {
        'states': [
            {
                'id': i,
                'items': sorted([fmt_item(item) for item in state])
            }
            for i, state in enumerate(states)
        ],
        'transitions': transitions,
        'start_state': 0,
        'augmented_start': aug_start,
        'num_states': len(states)
    }
