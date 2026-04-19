"""
Pretty-printers for every result dict returned by the library.

Every function in this module:
  - Accepts the result dict produced by a core function.
  - Prints a human-readable table / trace to stdout.
  - Returns the same dict (so it can be chained).

Usage:
    import compilerdesign as cd
    result = cd.lexical_analyzer(code)
    cd.show_lexical(result)
"""

from ._utils import EPSILON


# ---------------------------------------------------------------------------
#  Low level helpers
# ---------------------------------------------------------------------------

def _rule(char: str = "-", width: int = 72) -> str:
    return char * width


def _box(title: str, width: int = 72) -> str:
    bar = _rule("=", width)
    return f"{bar}\n  {title}\n{bar}"


def _table(rows, headers, pad: int = 2) -> str:
    """Render a simple ASCII table."""
    cols = len(headers)
    widths = [len(str(h)) for h in headers]
    for row in rows:
        for i in range(cols):
            widths[i] = max(widths[i], len(str(row[i])))
    widths = [w + pad for w in widths]

    def _fmt(row):
        return "| " + " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(row)) + " |"

    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    out = [sep, _fmt(headers), sep]
    out += [_fmt(r) for r in rows]
    out.append(sep)
    return "\n".join(out)


# ---------------------------------------------------------------------------
#  Lexical
# ---------------------------------------------------------------------------

def show_lexical(result: dict) -> dict:
    """Print lexical-analyzer output: token stream + summary."""
    print(_box("LEXICAL ANALYSIS"))
    rows = [(t["index"], t["type"], t["value"]) for t in result["token_stream"]]
    print(_table(rows, ("#", "TYPE", "VALUE")))

    print("\nSummary:")
    for k, v in result["summary"].items():
        print(f"  {k:<20} {v}")

    if result["unique_identifiers"]:
        print(f"\nIdentifiers : {', '.join(result['unique_identifiers'])}")
    if result["keywords_used"]:
        print(f"Keywords    : {', '.join(result['keywords_used'])}")
    return result


# ---------------------------------------------------------------------------
#  Grammar
# ---------------------------------------------------------------------------

def show_grammar(grammar: dict, title: str = "GRAMMAR") -> dict:
    """Render a grammar as `A -> p1 | p2 | ...`."""
    print(_box(title))
    for nt, prods in grammar.items():
        joined = " | ".join(prods) if prods else EPSILON
        print(f"  {nt:<6} -> {joined}")
    return grammar


def show_ambiguity(result: dict) -> dict:
    print(_box("AMBIGUITY CHECK"))
    print(f"  ambiguous : {result['ambiguous']}")
    print(f"  issues    : {result['issue_count']}")
    for issue in result["issues"]:
        print(f"    - {issue}")
    return result


# ---------------------------------------------------------------------------
#  FIRST / FOLLOW / LEADING / TRAILING
# ---------------------------------------------------------------------------

def _show_sets(sets: dict, label: str) -> None:
    rows = [(nt, "{ " + ", ".join(syms) + " }") for nt, syms in sets.items()]
    print(_table(rows, (label, "SET")))


def show_first_follow(result: dict) -> dict:
    print(_box("FIRST and FOLLOW"))
    _show_sets(result["FIRST"], "FIRST")
    print()
    _show_sets(result["FOLLOW"], "FOLLOW")
    return result


def show_leading_trailing(result: dict) -> dict:
    print(_box("LEADING and TRAILING"))
    _show_sets(result["LEADING"], "LEADING")
    print()
    _show_sets(result["TRAILING"], "TRAILING")
    return result


# ---------------------------------------------------------------------------
#  LL(1)
# ---------------------------------------------------------------------------

def show_ll1_table(result: dict) -> dict:
    print(_box("LL(1) PARSING TABLE"))
    rows = [(e["non_terminal"], e["terminal"], e["production"]) for e in result["entries"]]
    print(_table(rows, ("NT", "TERMINAL", "PRODUCTION")))
    print(f"\n  is_ll1    : {result['is_ll1']}")
    if result["conflicts"]:
        print("  conflicts :")
        for c in result["conflicts"]:
            print(f"    - {c}")
    return result


def show_parse_trace(result: dict, title: str = "PARSE TRACE") -> dict:
    print(_box(title))
    rows = [(s["step"], s["stack_display"], s["input_display"], s["action"]) for s in result["steps"]]
    print(_table(rows, ("#", "STACK", "INPUT", "ACTION")))
    print(f"\n  accepted : {result['accepted']}")
    if result.get("error"):
        print(f"  error    : {result['error']}")
    return result


# ---------------------------------------------------------------------------
#  LR(0)
# ---------------------------------------------------------------------------

def show_lr0(result: dict) -> dict:
    print(_box("LR(0) CANONICAL COLLECTION"))
    print(f"  augmented start : {result['augmented_start']}")
    print(f"  total states    : {result['num_states']}\n")
    for state in result["states"]:
        print(f"  State I{state['id']}:")
        for item in state["items"]:
            print(f"    {item}")
        print()
    print("Transitions:")
    rows = [(t["from_state"], t["symbol"], t["to_state"]) for t in result["transition_table"]]
    print(_table(rows, ("FROM", "SYMBOL", "TO")))
    return result


# ---------------------------------------------------------------------------
#  Expression conversions
# ---------------------------------------------------------------------------

def show_expression(expr: str, label: str = "EXPRESSION") -> str:
    print(f"  {label:<10} : {expr}")
    return expr


# ---------------------------------------------------------------------------
#  Symbol table / 3AC / DAG  (new modules)
# ---------------------------------------------------------------------------

def show_symbol_table(result: dict) -> dict:
    print(_box("SYMBOL TABLE"))
    rows = [
        (e["name"], e["type"], e["kind"], e["scope"], e["line"])
        for e in result["entries"]
    ]
    print(_table(rows, ("NAME", "TYPE", "KIND", "SCOPE", "LINE")))
    print(f"\n  total symbols : {result['total']}")
    return result


def show_three_address_code(result: dict) -> dict:
    print(_box("THREE-ADDRESS CODE"))
    rows = [(i, q["op"], q["arg1"], q["arg2"], q["result"]) for i, q in enumerate(result["quadruples"])]
    print(_table(rows, ("#", "OP", "ARG1", "ARG2", "RESULT")))
    print(f"\n  final result in : {result['final']}")
    return result


def show_dag(result: dict) -> dict:
    print(_box("DAG (Directed Acyclic Graph)"))
    rows = [(n["id"], n["label"], ",".join(map(str, n["children"])) or "-")
            for n in result["nodes"]]
    print(_table(rows, ("ID", "LABEL", "CHILDREN")))
    print(f"\n  root id : {result['root']}")
    print(f"  nodes   : {len(result['nodes'])}")
    return result
