import pathlib
import subprocess

import structlog

from .parse_repo_url import RepoURL


def clone(
    repo_url: RepoURL,
    no_act: bool,
    fetch: bool,
    prefix_path: pathlib.Path,
) -> None:
    log = structlog.get_logger()
    destination_path = prefix_path / repo_url.host / repo_url.group / repo_url.project
    if destination_path.exists() and fetch and repo_url.tool == "git":
        cmd = ["git", "fetch", "--all", "--prune", "--recurse-submodules"]
        log.info("run", cmd=cmd, cwd=destination_path)
        if not no_act:
            subprocess.run(cmd, check=True, cwd=str(destination_path))
        return

    path = str(prefix_path / repo_url.host / repo_url.group / repo_url.project)
    if repo_url.tool == "hg":
        cmd = ["hg", "clone", repo_url.url, path]
    else:
        cmd = [repo_url.tool, "clone", "--recurse-submodules", repo_url.url, path]
    log.info("run", cmd=cmd)
    if not no_act:
        subprocess.run(cmd, check=True)
