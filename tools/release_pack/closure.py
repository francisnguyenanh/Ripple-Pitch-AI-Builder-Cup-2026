"""Import closure over a candidate tree: for every Python file under the given roots, resolve `tests.*`, `tools.*` and top-level package imports that point INTO the tree and report the ones that are missing.
  python -m tools.release_pack.closure <candidate_dir> [--source-commit <sha>]
Used to decide which tracked files a selected test needs (add them from the same commit) instead of dropping or keeping directories by name. Reads files only."""
from __future__ import annotations

import argparse
import ast
import subprocess
import sys
from pathlib import Path

ROOTS = ("tests", "core/tests", "tools", "infra", "app", "core", "evals", "pitch", "reference_system", "providers", "registry", "ai_module")


def module_exists(base: Path, mod: str) -> bool:
    p = base / mod.replace(".", "/")
    return p.with_suffix(".py").exists() or (p / "__init__.py").exists() or p.is_dir()


def missing_imports(base: Path) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    tops = {d.name for d in base.iterdir() if d.is_dir()}
    for root in ROOTS:
        for f in (base / root).rglob("*.py") if (base / root).exists() else []:
            try:
                tree = ast.parse(f.read_text(encoding="utf-8"))
            except Exception:
                continue
            for n in ast.walk(tree):
                mods = []
                if isinstance(n, ast.Import):
                    mods = [a.name for a in n.names]
                elif isinstance(n, ast.ImportFrom) and n.level == 0 and n.module:
                    mods = [n.module] + [f"{n.module}.{a.name}" for a in n.names]
                for m in mods:
                    top = m.split(".")[0]
                    if top in tops and top in ("tests", "tools", "evals", "pitch", "reference_system", "infra", "core", "app", "providers", "registry", "ai_module") and not module_exists(base, m):
                        # `from pkg import name` where name is an attribute, not a module: only report when the package itself is absent or the parent module is absent
                        parent = m.rsplit(".", 1)[0]
                        if module_exists(base, parent) and "." in m and not (base / m.replace(".", "/")).exists() and not (base / (m.replace(".", "/") + ".py")).exists():
                            continue
                        out.setdefault(m, set()).add(str(f.relative_to(base)))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate")
    a = ap.parse_args()
    miss = missing_imports(Path(a.candidate))
    for m, who in sorted(miss.items()):
        print(m, "<-", len(who), "file(s), e.g.", sorted(who)[:2])
    print(f"missing modules: {len(miss)}")
    return 1 if miss else 0


if __name__ == "__main__":
    raise SystemExit(main())
