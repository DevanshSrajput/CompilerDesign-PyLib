"""
compilerdesign (cd) - A Python library for demonstrating compiler design concepts.

Usage:
    import compilerdesign as cd

    # Lexical Analysis
    result = cd.lexical_analyzer(source_code)

    # Grammar transformations
    new_grammar = cd.eliminate_left_recursion(grammar)
    new_grammar = cd.left_factoring(grammar)
    result = cd.check_ambiguity(grammar)

    # FIRST and FOLLOW sets
    result = cd.compute_first_follow(grammar, start='E')

    # LL(1) Parsing Table
    table = cd.build_ll1_table(grammar)
    parse_result = cd.ll1_parse(grammar, tokens)

    # Shift-Reduce Parsing
    result = cd.shift_reduce_parse(productions, tokens)

    # LEADING and TRAILING
    result = cd.compute_leading_trailing(grammar)

    # LR(0) Items
    result = cd.compute_lr0_items(productions, start='E')

    # Expression conversion
    postfix = cd.infix_to_postfix("a + b * c")
    prefix  = cd.infix_to_prefix("a + b * c")
    infix   = cd.postfix_to_infix("a b c * +")
    result  = cd.convert_expression("a + b * c", "infix", "postfix")
"""

__version__ = "1.0.0"
__author__ = "Adityaa"

# Lexical Analysis
from .lexical import lexical_analyzer

# Grammar Transformations
from .grammar import (
    eliminate_left_recursion,
    left_factoring,
    check_ambiguity,
)

# FIRST and FOLLOW
from .first_follow import (
    compute_first,
    compute_follow,
    compute_first_follow,
)

# LL(1) Predictive Parsing
from .ll1 import (
    build_ll1_table,
    ll1_parse,
)

# Shift-Reduce Parsing
from .shift_reduce import shift_reduce_parse

# LEADING and TRAILING
from .leading_trailing import (
    compute_leading,
    compute_trailing,
    compute_leading_trailing,
)

# LR(0) Items
from .lr0 import compute_lr0_items

# Intermediate Code Generation
from .intermediate_code import (
    infix_to_postfix,
    infix_to_prefix,
    postfix_to_infix,
    postfix_to_prefix,
    prefix_to_infix,
    prefix_to_postfix,
    convert_expression,
)

__all__ = [
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
    # Intermediate Code
    "infix_to_postfix",
    "infix_to_prefix",
    "postfix_to_infix",
    "postfix_to_prefix",
    "prefix_to_infix",
    "prefix_to_postfix",
    "convert_expression",
]
