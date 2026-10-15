"""Build the LOCAL submission candidate from a named commit: it never touches the development repository or its history.
  python -m tools.release_pack.make_candidate <out_dir> --commit <sha> --private-terms <file outside the repo>
Steps: (1) the owner's `tools.pitch_pack.export` selects tracked files by rule (needs that tool in the working copy); (2) this script adds the guide site, its builder and the release content from the SAME
commit, moves the development README to docs/EVALUATION_AND_HISTORY.md and installs the judge README; (3) the owner's publication scan (`tools.pitch_pack.scan`) and manifest
(`tools.pitch_pack.manifest`) run on the result. Exit 0 only when the scan is clean. Nothing is pushed or published."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

EXTRA_PREFIXES = ("site/", "tools/judge_site/", "tools/release_pack/", "docs/release/", "docs/judges/", "tools/build_baseline.py", "tests/ai7t0", "tests/ai8t0", "third_party/", "docs/verification/gate_G2.md", "docs/verification/h1_and_wiring_decisions.md", "docs/verification/cloud_readiness.md")


def git(*a: str) -> bytes:
    return subprocess.check_output(["git", *a])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("out_dir")
    ap.add_argument("--commit", default="HEAD")
    ap.add_argument("--private-terms", required=True)
    a = ap.parse_args()
    out = Path(a.out_dir).resolve()
    sha = git("rev-parse", a.commit).decode().strip()
    inv = out.parent / (out.name + "_INVENTORY.json")
    rc = subprocess.call([sys.executable, "-m", "tools.pitch_pack.export", str(out), "--commit", sha, "--inventory", str(inv)])
    if rc != 0:
        return rc
    paths = [p for p in git("ls-tree", "-r", "--name-only", "-z", sha).decode("utf-8").split("\0") if p]
    extra = []
    for p in paths:
        if p.startswith(EXTRA_PREFIXES) and not (out / p).exists():
            (out / p).parent.mkdir(parents=True, exist_ok=True)
            (out / p).write_bytes(git("show", f"{sha}:{p}"))
            extra.append(p)
    # (2b) import closure: a kept test or tool must find the helper modules it imports. Each addition is logged with the file that needs it (a decision by dependency, not by directory name).
    from tools.release_pack.closure import missing_imports
    tracked = set(paths)
    closure_log = []
    for _ in range(6):
        miss = missing_imports(out)
        added = 0
        for mod, who in sorted(miss.items()):
            if mod.split(".")[0] not in ("tests", "tools"):
                continue
            parts = mod.split(".")
            cands = []
            for k in range(len(parts), 1, -1):                 # the module itself, then its parents (`pkg.mod.name` may be an attribute of `pkg/mod.py`)
                base = "/".join(parts[:k])
                cands += [base + ".py"] + sorted(t for t in tracked if t.startswith(base + "/"))
            for c in cands:
                if c in tracked and not (out / c).exists():
                    (out / c).parent.mkdir(parents=True, exist_ok=True)
                    (out / c).write_bytes(git("show", f"{sha}:{c}"))
                    closure_log.append({"path": c, "reason": "imported by " + sorted(who)[0].replace("\\", "/")})
                    added += 1
        if not added:
            break
    # (2c) line endings: tests compare the Harbor fixture (stored CRLF, `-text`) with the demo bundle (stored LF); on a Windows checkout autocrlf hides that, on LF platforms the byte comparison fails. The attribute
    # makes a clone check the bundle input out with CRLF on every platform (blobs unchanged).
    ga = out / ".gitattributes"
    base_ = "ripple/_testdata/generated/bundles/harbor_demo/input/"
    # Only NAMED TEXT types get eol=crlf: a blanket rule on data/** also hit the three .xlsx workbooks (zip files), which git then rewrote on add/checkout and which no longer opened (found by running the README quickstart in a clone).
    text_types = ("csv", "jsonl", "json", "txt", "yaml", "yml", "md")
    rule = f"{base_}** -text\n" + "".join(f"{base_}{sub}/**/*.{ext} text eol=crlf\n{base_}{sub}/*.{ext} text eol=crlf\n" for sub in ("data", "run_output") for ext in text_types)
    ga.write_text((ga.read_text(encoding="utf-8") if ga.exists() else "") + ("\n" if ga.exists() else "") + "# release package: byte-identity of the Harbor sample on every platform (tests/pitch_brief/test_harbor_sim.py)\n" + rule, encoding="utf-8")
    # The development .gitignore hides `projects/*` and the shipped fixtures there were force-added; in a fresh `git init && git add .` of this package 13 required files would silently vanish (found by roundtrip.py).
    gi = out / ".gitignore"
    if gi.exists():
        import tempfile
        shipped = sorted(p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file())
        unignored: list[str] = []
        for _ in range(3):
            with tempfile.TemporaryDirectory() as t:
                Path(t, ".gitignore").write_bytes(gi.read_bytes())
                subprocess.run(["git", "init", "-q"], cwd=t, check=True)
                r = subprocess.run(["git", "check-ignore", "--no-index", "--stdin"], cwd=t, input=chr(10).join(shipped).encode("utf-8"), capture_output=True)  # bytes: text mode would add CR to every path on Windows
            hidden = [x for x in r.stdout.decode("utf-8").splitlines() if x]
            if not hidden:
                break
            rules = []
            for h in hidden:
                parts = h.split("/")
                rules += ["/".join(parts[:i]) + "/" for i in range(1, len(parts))] + [h]
            new = [f"!{x}" for x in dict.fromkeys(rules) if f"!{x}" not in unignored]
            unignored += new
            gi.write_text(gi.read_text(encoding="utf-8").rstrip("\n") + "\n" + ("\n# release package: shipped files that the development .gitignore hides (the development repository force-adds them)\n" if len(unignored) == len(new) else "") + "".join(n + "\n" for n in new), encoding="utf-8")
        if unignored:
            closure_log.append({"path": ".gitignore", "reason": f"{len(unignored)} un-ignore rule(s) so a fresh git add keeps the shipped files the development .gitignore hides (the development repository force-adds them)"})
    closure_log.append({"path": ".gitattributes", "reason": "added a text eol=crlf rule for the Harbor demo bundle input (tests compare it byte for byte with the CRLF fixture)"})
    # The files themselves are written with the bytes a checkout would produce (CRLF for the bundle's data and run_output), so a PLAIN COPY of this directory is correct on every platform and does not depend on
    # git configuration; the .gitattributes rule keeps a clone identical to it.
    converted = 0
    for sub in ("data", "run_output"):
        for f in (out / base_ / sub).rglob("*") if (out / base_ / sub).exists() else []:
            if f.is_file() and f.suffix.lstrip(".").lower() in text_types:
                b = f.read_bytes()
                if b"\x00" not in b[:8192] and b"\r\n" not in b:
                    f.write_bytes(b.replace(b"\n", b"\r\n"))
                    converted += 1
    closure_log.append({"path": base_ + "{data,run_output}/**", "reason": f"{converted} text file(s) written with CRLF line endings (byte-identical to the public Harbor fixture); no other content change"})
    transformations = []
    # (2d) private deployment identifiers in kept documents/tools: every term of the private-terms file (kept OUTSIDE the repository) found in the files listed here is replaced by a neutral placeholder
    # (candidate only; the development repository is not changed). The scanner files that define patterns are never touched.
    terms = [t.strip() for t in Path(a.private_terms).read_text(encoding="utf-8").splitlines() if t.strip() and not t.startswith("#")]
    for rel in ("docs/decisions/ADR-005-closed-loop-v2-architecture.md", "tools/judge_local/live_local.py"):
        f = out / rel
        if not f.exists():
            continue
        t = f.read_text(encoding="utf-8", errors="surrogateescape")
        n = 0
        for term in terms:
            if term in t:
                n += t.count(term)
                t = t.replace(term, "<private-identifier>")
        if n:
            f.write_text(t, encoding="utf-8", errors="surrogateescape")
            transformations.append({"path": rel, "change": f"{n} private identifier(s) replaced by a placeholder", "reason": "private deployment/operator identifier (terms file kept outside the repository)"})
    # (2e) markdown links to files that are not in the package become plain text with a note
    import re as _re
    fixed = 0
    for f in out.rglob("*.md"):
        if "_testdata" in f.parts or "node_modules" in f.parts:
            continue
        t = f.read_text(encoding="utf-8", errors="surrogateescape")

        def _fix(m):
            global_fixed = 0
            tgt = m.group(2).split("#")[0]
            if not tgt or tgt.startswith(("http://", "https://", "mailto:", "#")):
                return m.group(0)
            if (f.parent / tgt).exists():
                return m.group(0)
            return f"{m.group(1)} (not included in this package: `{tgt}`)"
        new = _re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", _fix, t)
        if new != t:
            f.write_text(new, encoding="utf-8", errors="surrogateescape")
            fixed += 1
    transformations.append({"path": "*.md", "change": f"{fixed} markdown file(s): links to files that are not in the package rewritten as text with a note", "reason": "no broken links"})
    # (2f) third-party notices: Python dependencies from the pinned requirements and the installed distribution metadata, plus vendored files
    from importlib import metadata as _md
    rows = []
    for line in (out / "requirements.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "==" not in line:
            continue
        name, pin = line.split("==", 1)
        try:
            d = _md.distribution(name)
            lic = (d.metadata.get("License-Expression") or d.metadata.get("License") or "").strip().splitlines()[0][:80] if (d.metadata.get("License-Expression") or d.metadata.get("License")) else ""
            if not lic:
                lic = "; ".join(c.split("::")[-1].strip() for c in (d.metadata.get_all("Classifier") or []) if c.startswith("License ::")) or "see the package metadata"
            rows.append(f"- {name}=={pin} - licence (from installed metadata, version {d.version}): {lic}")
        except Exception:
            rows.append(f"- {name}=={pin} - licence: not read (package not installed where the package was built); see its PyPI page")
    notice = ["# Third-party notices", "",
              "Generated at packaging time from `requirements.txt` and the installed distribution metadata; full licence texts ship inside each distribution. Frontend dependencies: `frontend/THIRD_PARTY_NOTICES.md`.", "",
              "## Python runtime dependencies", *rows, "",
              "## Vendored files", "- `templates/html/mermaid.min.js` - Mermaid 10.9.8 (`dist/mermaid.min.js`), verified byte-identical to the upstream npm release; MIT licence, Copyright (c) 2014 - 2022 Knut Sveidqvist. Text and provenance: `third_party/mermaid/LICENSE`, `third_party/mermaid/PROVENANCE.md`. The bundle contains libraries bundled by Mermaid's own build (D3, DOMPurify, dagre, KaTeX, khroma, ...) under their own licences.", "",
              "## Container base images (Dockerfile, site/Dockerfile)", "- Python base image and `nginxinc/nginx-unprivileged` (NGINX, BSD-2-Clause): see the image documentation for licence notices.", ""]
    (out / "THIRD_PARTY_NOTICES.md").write_text("\n".join(notice), encoding="utf-8")
    transformations.append({"path": "THIRD_PARTY_NOTICES.md", "change": "generated", "reason": "notices were a placeholder; Python dependencies and vendored Mermaid 10.9.8 (MIT, provenance verified) listed"})
    old = out / "README.md"
    if old.exists():
        (out / "docs").mkdir(exist_ok=True)
        old.replace(out / "docs" / "EVALUATION_AND_HISTORY.md")
    (out / "README.md").write_bytes((out / "docs" / "release" / "README_JUDGE.md").read_bytes())
    data = json.loads(inv.read_text(encoding="utf-8"))
    data["added_by_release_pack"] = extra
    data["added_by_import_closure"] = closure_log
    data["transformations"] = transformations
    data["source_commit"] = sha
    import hashlib
    here = Path(__file__).resolve().parents[1]
    data["tool_versions"] = {rel: hashlib.sha256((here / rel).read_bytes().replace(b"\r\n", b"\n")).hexdigest() for rel in ("release_pack/make_candidate.py", "release_pack/closure.py", "release_pack/roundtrip.py", "pitch_pack/export.py", "pitch_pack/scan.py", "pitch_pack/manifest.py", "pitch_pack/scan_allowlist.json")}
    data["tool_versions_note"] = "sha256 of each tool/rule file with LF line endings, taken from the working tree used for the build"
    data["readme"] = "docs/release/README_JUDGE.md installed as README.md; the development README is docs/EVALUATION_AND_HISTORY.md"
    inv.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
    allow = Path(__file__).resolve().parents[1] / "pitch_pack" / "scan_allowlist.json"
    scan_out = out.parent / (out.name + "_SCAN.txt")
    with open(scan_out, "w", encoding="utf-8") as fh:
        scan_rc = subprocess.call([sys.executable, "-m", "tools.pitch_pack.scan", str(out), "--private-terms", a.private_terms, "--allowlist", str(allow)], stdout=fh)
    print("scan report:", scan_out)
    rt_out = out.parent / (out.name + "_ROUNDTRIP.txt")
    with open(rt_out, "w", encoding="utf-8") as fh:
        rt_rc = subprocess.call([sys.executable, "-m", "tools.release_pack.roundtrip", str(out)], stdout=fh)
    print("git roundtrip:", "PASS" if rt_rc == 0 else "FAIL", "->", rt_out)
    subprocess.call([sys.executable, "-m", "tools.pitch_pack.manifest", str(out), "--out", str(out / "MANIFEST.json"), "--source-commit", sha])
    # the manifest alone must say how the export was made: source commit (already there), tool/rule versions, transformations, scan outcome; the export's checksum is its overall_sha256
    mpath = out / "MANIFEST.json"
    man = json.loads(mpath.read_text(encoding="utf-8"))
    man["build"] = {"tool_versions": data["tool_versions"], "transformations": data["transformations"], "scan_exit_code": scan_rc, "git_roundtrip": "PASS" if rt_rc == 0 else "FAIL",
                    "note": "overall_sha256 covers every file of the export except MANIFEST.json itself; tool_versions are sha256 of the builder, export, scan, manifest and allow-list files (LF-normalised)"}
    mpath.write_text(json.dumps(man, indent=1) + "\n", encoding="utf-8")
    print(f"candidate {out} from {sha}: kept {data['kept']} + extra {len(extra)}; scan exit {scan_rc}")
    return scan_rc or rt_rc


if __name__ == "__main__":
    raise SystemExit(main())
