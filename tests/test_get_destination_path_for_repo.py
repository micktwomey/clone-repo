from pathlib import Path

import pytest

from clone_repo.clone import get_destination_path_for_repo
from clone_repo.parse_repo_url import RepoURL

EXAMPLE_PREFIX_PATH = Path("/example/user/src")

EXAMPLES = (
    (
        RepoURL(
            "git@github.com:micktwomey/sync-camera-disk.git",
            "git",
            "github.com",
            "micktwomey",
            "sync-camera-disk",
        ),
        EXAMPLE_PREFIX_PATH / "github.com" / "micktwomey" / "sync-camera-disk",
    ),
    (
        RepoURL(
            "ssh://git@forgejo.example.com:2222/mick/my-project.git",
            "git",
            "forgejo.example.com:2222",
            "mick",
            "my-project",
        ),
        EXAMPLE_PREFIX_PATH / "forgejo.example.com_2222" / "mick" / "my-project",
    ),
)


@pytest.mark.parametrize("repo_url,expected_path", EXAMPLES)
def test_get_destination_path_for_repo(repo_url: RepoURL, expected_path: Path) -> None:
    assert (
        get_destination_path_for_repo(
            prefix_path=EXAMPLE_PREFIX_PATH, repo_url=repo_url
        )
        == expected_path
    )
