import nox


@nox.session()
def black(session: nox.Session) -> None:
    session.install(".")
    session.install("black")
    session.run("black", "--check", ".")


@nox.session()
def isort(session: nox.Session) -> None:
    session.install(".")
    session.install("isort")
    session.run("isort", "--check", ".")


@nox.session(python=["3.7", "3.8", "3.9", "3.10"])
def mypy(session: nox.Session) -> None:
    session.install(".")
    session.install("mypy", "nox", "pytest")
    session.run("mypy", ".")


@nox.session(python=["3.7", "3.8", "3.9", "3.10"])
def tests(session: nox.Session) -> None:
    session.install(".")
    session.install("pytest")
    session.run("pytest", "-vv", ".")
