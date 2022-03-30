# clone-repo: Easily clone repos

- [Home](https://github.com/micktwomey/clone-repo)
- [PyPI](https://pypi.org/project/clone-repo/)

## What is this?

For years I've been using a noddy script which clones many types of repos into a fixed location which is generated based on the repo itself. Similar to how go packages are cloned into go/src I typically clone my stuff into ~/src.

e.g. `clone-repo git@github.com:micktwomey/clone-repo.git` will clone using git to `~/src/github.com/micktwomey/clone-repo`.

This allows me to clone many different repos without worrying about stepping on each other. It also makes it easy to see where stuff comes from (e.g. `rm -rf ~/src/old.git.example.com` will wipe out clones from git server I don't use any more).

Install via `pip install clone-repo`.

Install with [pipx](https://pypa.github.io/pipx/) using `pipx install clone-repo` to make it available as a CLI tool everywhere.

Supports:

- `/path/to/repo`
  - `git clone` to `~/src/localhost/file/{repo}`
- `file:///path/to/repo`
  - `git clone` to `~/src/localhost/file/{repo}`
- `git@example.com:org/repo.git`
  - `git clone` to `~/src/{host}/{org}/{repo}`
- `https://github.com/org/repo.git`
  - `git clone` to `~/src/github.com/{org}/{repo}`
- `https://gitlab.example.com/org/repo.git`
  - `git clone` to `~/src/{host}/{org}/{repo}`
- `https://hg.mozilla.org/mozilla-central/`
  - `hg clone` to `~/src/hg.mozilla.org/{org}/{repo}`
- `https://hg.sr.ht/~org/repo`
  - `hg clone` to `~/src/hg.sr.ht/{org}/{repo}`
- `keybase://team/org/repo`
  - `git clone` to `~/src/keybase/{org}/{repo}`
- `man@man.sr.ht:~org/repo`
  - `git clone` to `~/src/man.sr.ht/{org}/{repo}`
- `ssh://git@example.com:7999/somegroup/myrepo.git`
  - `git clone` to `~/src/{host}/{org}/{repo}`
- `ssh://hg@bitbucket.org/org/repo`
  - `hg clone` to `~/src/{host}/{org}/{repo}`

For `https://` URLs the default is git but some will behave differently based on the domain.

# Development

If you want to quickly develop you can use [poetry](https://python-poetry.org) and [pytest](https://pytest.org/):

1. `poetry install`
2. `pytest -vv`

If you want to test across all supported Python versions you can install them via [asdf](https://asdf-vm.com) and then use [nox](https://nox.thea.codes):

1. `asdf install`
2. `poetry install`
3. `nox`

If you want to run [pre-commit](https://pre-commit.com) hooks before committing:

1. `poetry install`
2. `pre-commit install`

Finally, there is a [just](https://github.com/casey/just) justfile to run some commands.
