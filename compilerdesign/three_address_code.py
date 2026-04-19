"""
Three-Address Code (3AC) generation from an infix expression.

Converts expressions like  `a + b * c - d`  into a list of quadruples:
    t1 = b * c
    t2 = a + t1
    t3 = t2 - d

Result dict:
  {
    'quadruples': [ {op, arg1, arg2, result}, ... ],
    'final':      't3',               # name of the last temporary
    'pretty':     ['t1 = b * c', ...] # ready-to-print lines
  }
"""

from .intermediate_code import infix_to_postfix, PRECEDENCE


def generate_three_address_code(expr: str) -> dict:
    """Build 3AC (quadruples) for an infix arithmetic expression."""
    postfix = infix_to_postfix(expr).split()
    stack = []
    quads = []
    counter = 0

    for token in postfix:
        if token in PRECEDENCE:
            if len(stack) < 2:
                raise ValueError(f"Malformed expression near '{token}'")
            b = stack.pop()
            a = stack.pop()
            counter += 1
            temp = f"t{counter}"
            quads.append({"op": token, "arg1": a, "arg2": b, "result": temp})
            stack.append(temp)
        else:
            stack.append(token)

    if len(stack) != 1:
        raise ValueError("Invalid expression: operands left on stack")

    pretty = [f"{q['result']} = {q['arg1']} {q['op']} {q['arg2']}" for q in quads]
    return {"quadruples": quads, "final": stack[0], "pretty": pretty}
