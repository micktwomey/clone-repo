project := "clone_repo"

default: pre-commit lint coverage

test: pytest

# Run pytest
pytest *ARGS="-vv":
    poetry run pytest {{ARGS}}

# Run pytest with coverage
coverage *ARGS=("-vv --cov=" + project + " --cov-report=html --cov-report=term --cov-branch --cov-context=test"):
    poetry run pytest {{ARGS}}

# Run all linting actions
lint: ruff mypy black

# Lint code with ruff
ruff COMMAND="check" *ARGS=".":
    poetry run ruff {{COMMAND}} {{ARGS}}

# Check code with Mypy
mypy *ARGS=".":
    poetry run mypy {{ARGS}}

# Check files with black
black *ARGS=".":
    poetry run black {{ARGS}}

# Run pre-commit
pre-commit COMMAND="run" *ARGS="--all-files":
    poetry run pre-commit {{COMMAND}} {{ARGS}}

# Add a CHANGELOG.md entry, e.g. just changelog-add added "My entry"
changelog-add TYPE ENTRY:
    poetry run changelog-manager add {{TYPE}} "{{ENTRY}}"

# Install and bootstrap your dev env, usually a one off
bootstrap-dev-env:
    asdf install
    poetry install
    poetry run pre-commit install

# Find out what your next released version might be based on the changelog.
next-version:
    poetry run changelog-manager suggest

# Build and create files for a release
prepare-release:
    #!/bin/bash
    set -xeuo pipefail
    poetry run changelog-manager release
    poetry version $(poetry run changelog-manager current)
    rm -rvf dist
    poetry build

# Tag and release files, make sure you run 'just prepare-release' first.
do-release:
    #!/bin/bash
    set -xeuo pipefail
    VERSION=$(poetry run changelog-manager current)
    POETRY_VERSION=$(poetry version -s)
    if [ "${VERSION}" != "${POETRY_VERSION}" ]; then
        echo "Mismatch between changelog version ${VERSION} and poetry version ${VERSION}"
        exit 1
    fi
    git add pyproject.toml CHANGELOG.md
    mkdir -p build
    poetry run changelog-manager display --version $VERSION > build/release-notes.md
    if [ ! -f dist/{{project}}-${VERSION}.tar.gz ]; then
        echo "Missing expected file in dist, did you run 'just prepare-release'?"
        exit 1
    fi
    poetry publish --dry-run
    git commit -m"Release ${VERSION}"
    git tag $VERSION
    git push origin $VERSION
    git push origin main
    gh release create $VERSION --title $VERSION -F build/release-notes.md ./dist/*
    poetry publish
    rm -rvf ./dist
