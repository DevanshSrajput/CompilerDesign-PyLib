# Changes

All substantive edits made during the v1.0.1 → v1.1.0 overhaul.

---

## 1.0.2 — Design improvement release

### Changed

- Design improvements to the project presentation/documentation assets.
- Version bumped to **1.0.2** for the PyPI release.

---

## 1.0.2 — Library overhaul

### New modules

- **`compilerdesign/display.py`** — pretty-printers for every result
  object the library produces. One function per topic:
  `show_lexical`, `show_grammar`, `show_ambiguity`, `show_first_follow`,
  `show_leading_trailing`, `show_ll1_table`, `show_parse_trace`,
  `show_lr0`, `show_expression`, `show_symbol_table`,
  `show_three_address_code`, `show_dag`. Each renders a clean ASCII
  table / trace and **returns the input unchanged** so it can be chained.
- **`compilerdesign/symbol_table.py`** — new `build_symbol_table(code)`
  that scans C-like source and collects functions, parameters and
  variables with scope and line number.
- **`compilerdesign/three_address_code.py`** — new
  `generate_three_address_code(expr)` that builds quadruples (3AC) from
  an infix arithmetic expression, with ready-to-print lines.
- **`compilerdesign/dag.py`** — new `build_dag(expr)` that constructs a
  DAG of an arithmetic expression, automatically sharing common
  sub-expressions.

### Public API additions (re-exported on `compilerdesign`)

- `build_symbol_table`, `generate_three_address_code`, `build_dag`
- All `show_*` pretty-printers listed above

### Removed / cleaned up

- Deleted the stale duplicate modules that lived at the project root
  (`lexical.py`, `grammar.py`, `first_follow.py`, `leading_trailing.py`,
  `ll1.py`, `lr0.py`, `shift_reduce.py`, `intermediate_code.py`) and the
  stray root-level `__init__.py`. They were an older copy never used by
  the packaged library (`pyproject.toml` only ships
  `compilerdesign/`) and drifted from the canonical package versions
  (e.g. old root `lexical.py` lacked the deterministic
  `sorted_unique` output used by tests). Keeping them around caused
  confusion about which file was authoritative.
- Result: a single source of truth inside `compilerdesign/`.

### Packaging

- Bumped version **1.0.1 → 1.0.2** in `pyproject.toml` and
  `compilerdesign/__init__.py`.
- Expanded the `description` in `pyproject.toml` to reflect the new
  modules.

### Documentation

- **`DOCUMENTATION.md`** (new) — full walk-through of every module with
  input format, example code and example output. Includes a
  pretty-printer cheat-sheet and an end-to-end example.
- **`CHANGES.md`** (this file, new) — change log for every future release.
- **`README.md`** rewritten as a concise landing page that links to
  `DOCUMENTATION.md` for details and showcases the new `show_*`
  pretty-printer pattern, the symbol table, 3AC and DAG.
- `help()` output updated to list the new functions and the pretty-printer
  convention.

### Tests

- `test_all.py` extended with tests for the three new modules
  (`build_symbol_table`, `generate_three_address_code`, `build_dag`)
  and a smoke test that every `show_*` function runs without raising.
- The existing assertion `"compilerdesign v1.0.1"` updated to
  `"compilerdesign v1.1.0"`.

### Behaviour preserved

- No change to the signature or return value of any existing function.
- No change to how grammars / productions / tokens are provided.
- All 12 tests from the previous version still pass.
