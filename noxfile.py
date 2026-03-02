import nox

nox.options.sessions = ("tests",)
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = True


@nox.session(python=("3.10", "3.11", "3.12", "3.13", "3.14"))
@nox.parametrize("django", ("4.2", "5.2", "6.0"))
def tests(session, django):
    # Django 6.0 requires Python 3.12+
    if django == "6.0" and session.python in ("3.10", "3.11"):
        session.skip()
    major, minor = (int(x) for x in django.split("."))
    session.install("poetry")
    session.install(f"django>={django},<{major}.{minor + 1}")
    session.install("factory-boy>=3,<4")
    session.run(
        "poetry",
        "install",
        # this is necessary to prevent poetry from creating
        # its own virtualenv
        env={"VIRTUAL_ENV": session.virtualenv.location},
    )
    session.run("pytest")


@nox.session(python="3.12")
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


@nox.session(python="3.12")
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
