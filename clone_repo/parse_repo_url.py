"""Parse git/hd/other repo urls into a neat usable format

Tries to handle all the exotic repos, suitable for cloning.

"""

import dataclasses
import pathlib
import re
import typing


@dataclasses.dataclass
class RepoURL:
    url: str
    tool: str
    host: str
    group: str
    project: str


def parse_url(url: str) -> typing.Optional[RepoURL]:
    """Parses the given repo url"""
    if url.startswith("file://") or str(pathlib.Path(url).expanduser()).startswith("/"):
        return RepoURL(url, "git", "localhost", "file", pathlib.Path(url).name)

    m = re.match(
        r"(?P<tool>[^:@]+)(://|@)(?P<tool_user>hg@|git@){0,1}(?P<host>[^/:]+):{0,1}(?P<port>[0-9]+){0,1}(/|:)((?P<group>[^/]+)/){0,1}(?P<project>.+)",
        url,
    )
    if m is None:
        return None
    matched = m.groupdict()
    tool = matched["tool"]
    tool_user = matched.get("tool_user", None)
    if tool == "ssh":
        if tool_user == "hg@":
            tool = "hg"
        else:
            tool = "git"
    if tool in ("keybase", "https", "man"):
        tool = "git"
    host = matched["host"]
    if host.startswith("hg."):
        tool = "hg"
    port = matched.get("port", None)
    if port is not None:
        host = "{}:{}".format(host, port)
    if matched["tool"] == "keybase":
        host = "keybase"
    group = matched["group"]
    if group is None:
        group = ""
    project = re.split(r"\.git$", matched["project"])[0]
    if project.endswith("/"):
        project = project[:-1]
    return RepoURL(url, tool, host, group, project)
