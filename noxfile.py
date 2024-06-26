import nox

nox.options.sessions = ("tests",)
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = True


@nox.session(python=("3.8", "3.9", "3.10", "3.11", "3.12"))
@nox.parametrize("django", ("3.2", "4.2", "5.0"))
def tests(session, django):
    if django == "5.0" and session.python in ("3.8", "3.9"):
        session.skip()
    session.install("poetry")
    session.install(f"django>={django},<{django}.999")
    session.install("factory-boy>=2.9.2,<2.9.99999")
    session.run(
        "poetry",
        "install",
        # this is necessary to prevent poetry from creating
        # its own virtualenv
        env={"VIRTUAL_ENV": session.virtualenv.location},
    )
    session.run("pytest")


@nox.session(python="3.8")
def docs(session):
    session.install("poetry")
    session.run(
        "poetry",
        "install",
        # this is necessary to prevent poetry from creating
        # its own virtualenv
        env={"VIRTUAL_ENV": session.virtualenv.location},
    )

    session.run("sphinx-build", "docs", "docs/_build/html")


@nox.session(python=False)
def clean_docs(session):
    session.run("rm", "-rf", "docs/_build")


@nox.session(python="3.8")
def release_test(session):
    session.install("poetry", "twine")
    session.run(
        "poetry",
        "build",
        # this is necessary to prevent poetry from creating
        # its own virtualenv
        env={"VIRTUAL_ENV": session.virtualenv.location},
    )
    session.run("twine", "check", "dist/*")
