"""Git round-trip check of a built candidate: the byte-sensitive parts must survive `git add` + `git clone` unchanged.

  python -m tools.release_pack.roundtrip <candidate_dir>

Copies the candidate to a temp dir, commits it, clones it with core.autocrlf=false and with core.autocrlf=true, and compares the bytes of every file under
the byte-sensitive trees with the candidate. A `.gitattributes` rule that touches a binary file (an .xlsx rewritten by `text eol=crlf`) fails here.
Exit 0 only if every compared file is identical in both clones. Nothing is read from or written to the candidate.
"""
from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TREES = ("ripple/_testdata/generated/bundles/harbor_demo/input", "fixtures", "reference_system", "projects")


def _git(args: list[str], cwd: Path) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _digests(root: Path) -> dict[str, str]:
    out = {}
    for t in TREES:
        base = root / t
        if base.exists():
            for f in base.rglob("*"):
                if f.is_file():
                    out[f.relative_to(root).as_posix()] = hashlib.sha256(f.read_bytes()).hexdigest()
    return out


def main(argv: list[str] | None = None) -> int:
    cand = Path((argv or sys.argv[1:])[0]).expanduser().resolve()
    want = _digests(cand)
    tmp = Path(tempfile.mkdtemp(prefix="roundtrip_"))
    try:
        src = tmp / "src"
        shutil.copytree(cand, src, ignore=shutil.ignore_patterns(".git", "__pycache__", "node_modules"))
        _git(["init", "-q", "-b", "main"], src)
        _git(["-c", "core.autocrlf=false", "add", "-A"], src)
        _git(["-c", "core.autocrlf=false", "-c", "user.name=t", "-c", "user.email=noreply@example.com", "commit", "-q", "-m", "x"], src)
        # With core.autocrlf=true git may legitimately rewrite line endings of files that carry no `text` attribute (ordinary source text); every file with an explicit text/-text attribute must stay identical.
        r = subprocess.run(["git", "check-attr", "text", "--stdin"], cwd=src, input=chr(10).join(want).encode("utf-8"), capture_output=True)  # bytes: text mode would add CR to every path on Windows
        protected = {line.rsplit(": text: ", 1)[0] for line in r.stdout.decode("utf-8").splitlines() if not line.endswith(": unspecified")}
        bad = 0
        for mode in ("false", "true"):
            _git(["-c", f"core.autocrlf={mode}", "clone", "-q", str(src), f"clone_{mode}"], tmp)
            got = _digests(tmp / f"clone_{mode}")
            diff = sorted(p for p in want if got.get(p) != want[p] and (mode == "false" or p in protected))
            missing = [p for p in diff if p not in got]
            print(f"autocrlf={mode}: {len(want) if mode == 'false' else len(protected)} files compared, {len(diff)} differ ({len(missing)} missing in the clone)" + ("" if not diff else ": " + ", ".join(diff[:20])))
            bad += len(diff)
        print("roundtrip", "PASS" if not bad else "FAIL")
        return 1 if bad else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
