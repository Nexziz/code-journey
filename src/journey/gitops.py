"""The git side: a local bare repository that grades pushes, and the workspace you push from.

The bare repository is your private "vogsphere". A post-receive hook runs the grader on every
push, and git relays the hook's output to your terminal as `remote: ...` lines.
"""

from __future__ import annotations

import io
import shlex
import subprocess
import sys
import tarfile
from pathlib import Path

WORKSPACE_GITIGNORE = """\
# Build output: your solutions are source files, so keep binaries out of git.
a.out
*.o
*.dSYM/
__pycache__/
*.pyc
"""


class GitError(Exception):
    pass


def git(*args: str, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    try:
        proc = subprocess.run(
            ["git", *args], cwd=cwd, capture_output=True, text=True, stdin=subprocess.DEVNULL
        )
    except FileNotFoundError as exc:
        raise GitError("git is not installed") from exc
    if check and proc.returncode != 0:
        raise GitError(f"git {' '.join(args)}: {proc.stderr.strip() or proc.stdout.strip()}")
    return proc


def ensure_remote(remote: Path) -> None:
    if not (remote / "HEAD").exists():
        remote.parent.mkdir(parents=True, exist_ok=True)
        git("init", "--bare", "-b", "main", str(remote))


def hook_script(home: Path) -> str:
    package_parent = Path(__file__).resolve().parent.parent
    return (
        "#!/bin/sh\n"
        "# Written by `journey init`. It grades whatever you push. Run `journey init` to refresh.\n"
        f"JOURNEY_HOME={shlex.quote(str(home))}\n"
        f"PYTHONPATH={shlex.quote(str(package_parent))}${{PYTHONPATH:+:$PYTHONPATH}}\n"
        "JOURNEY_COLOR=1\n"
        "export JOURNEY_HOME PYTHONPATH JOURNEY_COLOR\n"
        f"exec {shlex.quote(sys.executable)} -m journey _hook\n"
    )


def hook_path(remote: Path) -> Path:
    return remote / "hooks" / "post-receive"


def install_hook(remote: Path, home: Path) -> Path:
    path = hook_path(remote)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(hook_script(home))
    path.chmod(0o755)
    return path


def ensure_workspace(workspace: Path, remote: Path) -> None:
    workspace.mkdir(parents=True, exist_ok=True)
    if not (workspace / ".git").exists():
        git("init", "-b", "main", cwd=workspace)
    remotes = git("remote", cwd=workspace).stdout.split()
    verb = "set-url" if "origin" in remotes else "add"
    git("remote", verb, "origin", str(remote), cwd=workspace)
    # `git commit` refuses to run without an identity; give a fallback only if none is set.
    if git("config", "user.email", cwd=workspace, check=False).returncode != 0:
        git("config", "user.name", "Journey Student", cwd=workspace)
        git("config", "user.email", "student@journey.local", cwd=workspace)
    ignore = workspace / ".gitignore"
    if not ignore.exists():
        ignore.write_text(WORKSPACE_GITIGNORE)


def export_dir(remote: Path, rev: str, subdir: str, dest: Path) -> Path | None:
    """Extract `subdir` as it was in commit `rev`. Returns its path, or None if it is not there."""
    proc = subprocess.run(
        ["git", "--git-dir", str(remote), "archive", "--format=tar", rev, "--", subdir],
        capture_output=True,
    )
    if proc.returncode != 0:
        return None
    with tarfile.open(fileobj=io.BytesIO(proc.stdout)) as tar:
        try:
            tar.extractall(dest, filter="data")
        except TypeError:  # Python without extraction filters
            tar.extractall(dest)
    return dest / subdir
