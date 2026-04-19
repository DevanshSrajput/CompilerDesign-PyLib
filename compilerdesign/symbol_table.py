"""
Symbol-table construction from C-like source code.

Very small heuristic scanner; intended for teaching. It recognises:
  - variable declarations:   int x;   float y = 3.14;
  - function declarations:   int foo(int a, float b) { ... }
  - scope (global / function body) from `{` and `}`

Result dict:
  {
    'entries': [ {name, type, kind, scope, line}, ... ],
    'total':   <int>,
  }
"""

import re

_TYPES = r"(int|float|double|char|void|long|short|unsigned|signed)"
_NAME = r"[A-Za-z_]\w*"

_FUNC_RE = re.compile(rf"\b{_TYPES}\s+({_NAME})\s*\(([^)]*)\)\s*\{{")
_VAR_RE = re.compile(rf"\b{_TYPES}\s+({_NAME})(\s*=\s*[^;,]+)?\s*[;,]")


def build_symbol_table(code: str) -> dict:
    """Scan source and return a symbol table."""
    entries = []
    scope_stack = ["global"]
    line_no = 0

    for raw_line in code.splitlines():
        line_no += 1
        line = raw_line.strip()

        func_match = _FUNC_RE.search(raw_line)
        if func_match:
            ftype, fname, params = func_match.groups()
            entries.append({
                "name": fname,
                "type": ftype,
                "kind": "function",
                "scope": scope_stack[-1],
                "line": line_no,
            })
            scope_stack.append(fname)
            for p in params.split(","):
                p = p.strip()
                if not p:
                    continue
                parts = p.split()
                if len(parts) >= 2:
                    entries.append({
                        "name": parts[-1].lstrip("*"),
                        "type": " ".join(parts[:-1]),
                        "kind": "parameter",
                        "scope": fname,
                        "line": line_no,
                    })
            continue

        for m in _VAR_RE.finditer(raw_line):
            vtype, vname, _init = m.groups()
            entries.append({
                "name": vname,
                "type": vtype,
                "kind": "variable",
                "scope": scope_stack[-1],
                "line": line_no,
            })

        for ch in line:
            if ch == "{":
                if not func_match:
                    scope_stack.append(f"block@{line_no}")
            elif ch == "}":
                if len(scope_stack) > 1:
                    scope_stack.pop()

    seen = set()
    unique = []
    for e in entries:
        key = (e["name"], e["scope"], e["kind"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(e)

    return {"entries": unique, "total": len(unique)}
