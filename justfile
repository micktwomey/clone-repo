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
