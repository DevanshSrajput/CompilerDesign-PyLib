"""
DAG (Directed Acyclic Graph) construction for an arithmetic expression.

Common sub-expressions share a single node, so redundant computations become
visible. Uses postfix evaluation and deduplicates by (label, left, right).

Result dict:
  {
    'nodes': [ {id, label, children:[int,...]}, ... ],
    'root':  <int>,
  }
"""

from .intermediate_code import infix_to_postfix, PRECEDENCE


def build_dag(expr: str) -> dict:
    postfix = infix_to_postfix(expr).split()
    stack = []
    nodes = []
    lookup = {}

    def _add(label, children):
        key = (label, tuple(children))
        if key in lookup:
            return lookup[key]
        node_id = len(nodes)
        nodes.append({"id": node_id, "label": label, "children": list(children)})
        lookup[key] = node_id
        return node_id

    for token in postfix:
        if token in PRECEDENCE:
            if len(stack) < 2:
                raise ValueError(f"Malformed expression near '{token}'")
            right = stack.pop()
            left = stack.pop()
            stack.append(_add(token, [left, right]))
        else:
            stack.append(_add(token, []))

    if len(stack) != 1:
        raise ValueError("Invalid expression")

    return {"nodes": nodes, "root": stack[0]}
