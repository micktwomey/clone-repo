import json
import pathlib
import subprocess
import sys
import tempfile
import typing

import pytest


@pytest.fixture
def prefix() -> typing.Iterator[str]:
    with tempfile.TemporaryDirectory() as tempdir:
        # Replicate the resolve calls to ensure our check matches the path used in
        # clone-repo.
        temp_path = pathlib.Path(tempdir).expanduser().resolve()
        yield str(temp_path)


def test_help(capfd: pytest.CaptureFixture[str]) -> None:
    subprocess.check_call([sys.executable, "-m", "clone_repo.main", "--help"])
    captured = capfd.readouterr()
    assert "Usage: python -m clone_repo.main [OPTIONS] URL" in captured.out


def test_json_dry_run(capfd: pytest.CaptureFixture[str], prefix: str) -> None:
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "clone_repo.main",
            "--json",
            "--no-act",
            "--verbose",
            "--prefix",
            prefix,
            "git@github.com:micktwomey/clone-repo.git",
        ]
    )
    captured = capfd.readouterr()
    output = json.loads(captured.out)
    assert "timestamp" in output
    del output["timestamp"]
    assert output == {
        "cmd": [
            "git",
            "clone",
            "--recurse-submodules",
            "git@github.com:micktwomey/clone-repo.git",
            f"{prefix}/github.com/micktwomey/clone-repo",
        ],
        "debug": False,
        "event": "run",
        "fetch": False,
        "json": True,
        "level": "info",
        "no_act": True,
        "prefix": f"PosixPath('{prefix}')",
        # "timestamp": "2022-03-28T11:05:00.367341Z",
        "url": "git@github.com:micktwomey/clone-repo.git",
        "verbose": True,
    }


def test_clone(capfd: pytest.CaptureFixture[str], prefix: str) -> None:
    source_path = pathlib.Path(prefix) / "repo"
    source_path.mkdir()
    with (source_path / "hello.txt").open("wt") as fp:
        fp.write("Hello there")
    subprocess.check_call(["git", "init"], cwd=source_path)
    subprocess.check_call(["git", "add", "hello.txt"], cwd=source_path)
    subprocess.check_call(["git", "commit", "-m", "Write a greeting"], cwd=source_path)
    print(capfd.readouterr())  # flush the buffer

    # clone
    dest_path = pathlib.Path(prefix) / "dest"
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "clone_repo.main",
            "--json",
            "--verbose",
            "--prefix",
            str(dest_path),
            str(source_path),
        ]
    )
    assert (dest_path / "localhost/file/repo/hello.txt").is_file()
    assert (dest_path / "localhost/file/repo/hello.txt").open(
        "rt"
    ).read() == "Hello there"
