"""
compilerdesign  (import as ``cd``)

A teaching library for the core topics of a compiler-design course.

Every function returns a plain ``dict`` / ``str`` so you can inspect the raw
data, AND there is a matching ``show_*`` pretty-printer for every result,
so you can also see clean, tabular output in one call:

    import compilerdesign as cd

    result = cd.lexical_analyzer(source_code)
    cd.show_lexical(result)          # prints a nice table

See DOCUMENTATION.md for the full walk-through.
"""

__version__ = "1.1.0"
__author__ = "Aditya"
__github__ = "aditya-ig10"


# ---- core modules ---------------------------------------------------------
from .first_follow import compute_first, compute_first_follow, compute_follow
from .grammar import check_ambiguity, eliminate_left_recursion, left_factoring
from .intermediate_code import (
    convert_expression,
    infix_to_postfix,
    infix_to_prefix,
    postfix_to_infix,
    postfix_to_prefix,
    prefix_to_infix,
    prefix_to_postfix,
)
from .leading_trailing import compute_leading, compute_leading_trailing, compute_trailing
from .lexical import lexical_analyzer
from .ll1 import build_ll1_table, ll1_parse
from .lr0 import compute_lr0_items
from .shift_reduce import shift_reduce_parse

# ---- new in 1.1.0 ---------------------------------------------------------
from .symbol_table import build_symbol_table
from .three_address_code import generate_three_address_code
from .dag import build_dag
from .display import (
    show_lexical,
    show_grammar,
    show_ambiguity,
    show_first_follow,
    show_leading_trailing,
    show_ll1_table,
    show_parse_trace,
    show_lr0,
    show_expression,
    show_symbol_table,
    show_three_address_code,
    show_dag,
)


def help() -> str:
    """Print a short overview of the library and its public API."""
    message = f"""
compilerdesign v{__version__}

A teaching library for core compiler-design topics.

Core functions (return dict / str):
  lexical_analyzer(code)
  eliminate_left_recursion(grammar) | left_factoring(grammar) | check_ambiguity(grammar)
  compute_first(grammar) | compute_follow(grammar, start) | compute_first_follow(grammar, start)
  compute_leading(grammar) | compute_trailing(grammar) | compute_leading_trailing(grammar)
  build_ll1_table(grammar, start) | ll1_parse(grammar, tokens, start)
  shift_reduce_parse(productions, tokens)
  compute_lr0_items(productions, start)
  infix_to_postfix / infix_to_prefix / postfix_to_infix / prefix_to_infix
  convert_expression(expr, from_notation, to_notation)
  build_symbol_table(code)                       # NEW
  generate_three_address_code(expr)              # NEW
  build_dag(expr)                                # NEW

Pretty-printers (print a table, return the same dict):
  show_lexical, show_grammar, show_ambiguity,
  show_first_follow, show_leading_trailing,
  show_ll1_table, show_parse_trace, show_lr0,
  show_symbol_table, show_three_address_code, show_dag

Quick start:
    import compilerdesign as cd
    cd.show_lexical(cd.lexical_analyzer("int x = 10;"))

Author: {__author__}
GitHub: https://github.com/{__github__}
""".strip()
    print(message)
    return message


__all__ = [
    "help",
    # Lexical
    "lexical_analyzer",
    # Grammar
    "eliminate_left_recursion",
    "left_factoring",
    "check_ambiguity",
    # FIRST / FOLLOW
    "compute_first",
    "compute_follow",
    "compute_first_follow",
    # LL(1)
    "build_ll1_table",
    "ll1_parse",
    # Shift-Reduce
    "shift_reduce_parse",
    # Leading / Trailing
    "compute_leading",
    "compute_trailing",
    "compute_leading_trailing",
    # LR(0)
    "compute_lr0_items",
    # Intermediate code (expression conversion)
    "infix_to_postfix",
    "infix_to_prefix",
    "postfix_to_infix",
    "postfix_to_prefix",
    "prefix_to_infix",
    "prefix_to_postfix",
    "convert_expression",
    # New in 1.1.0
    "build_symbol_table",
    "generate_three_address_code",
    "build_dag",
    # Pretty-printers
    "show_lexical",
    "show_grammar",
    "show_ambiguity",
    "show_first_follow",
    "show_leading_trailing",
    "show_ll1_table",
    "show_parse_trace",
    "show_lr0",
    "show_expression",
    "show_symbol_table",
    "show_three_address_code",
    "show_dag",
]
