default: pytest

pytest *ARGS='-vv':
    pytest {{ARGS}}

nox *ARGS:
    nox {{ARGS}}

# Add a CHANGELOG.md entry, e.g. just changelog-add added "My entry"
changelog-add TYPE ENTRY:
    changelog-manager add {{TYPE}} {{ENTRY}}

# Install and bootstrap your dev env, usually a one off
bootstrap-dev-env:
    asdf install
    poetry install
    pre-commit install

# Build and create files for a release
prepare-release:
    #!/bin/bash
    set -xeuo pipefail
    changelog-manager release
    poetry version $(changelog-manager current)
    rm -rvf dist
    poetry build

# Tag and release files
do-release:
    #!/bin/bash
    set -xeuo pipefail
    VERSION=$(changelog-manager current)
    POETRY_VERSION=$(poetry version -s)
    if [ "${VERSION}" != "${POETRY_VERSION}" ]; then
        echo "Mismatch between changelog version ${VERSION} and poetry version ${VERSION}"
        exit 1
    fi
    git add pyproject.toml CHANGELOG.md
    mkdir -p build
    changelog-manager display --version $VERSION > build/release-notes.md
    if [ ! -f dist/clone-repo-${VERSION}.tar.gz ]; then
        echo "Missing expected file in dist, did you run 'just prepare-release'?"
        exit 1
    fi
    poetry publish --dry-run
    git commit -m"Release ${VERSION}"
    git tag $VERSION
    git push origin $VERSION
    gh release create $VERSION --title $VERSION -F build/release-notes.md ./dist/*
    poetry publish
    rm -rvf ./dist
