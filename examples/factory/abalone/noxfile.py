# type: ignore
# This is a test file, skipping type checking in it.
"""Check code in sources, tests, scripts and notebooks."""
from os.path import abspath, dirname
from shutil import rmtree

import nox

PROJECT_NAME = "abalone"
PACKAGE_NAME = "abalone"
REPO_ROOT_PATH = dirname(abspath(__file__))

VENV_BACKEND = "venv"

PYTHON_VERSION = "3.9"

nox.options.stop_on_first_error = True

# nox.options.sessions = ['lint', 'tests']
nox.options.sessions = ["format", "lint", "md_lint", "mypy", "unit_tests", "docs"]

nox.options.envdir = ".venv"
# nox.options.reuse_existing_virtualenvs = True
nox.options.reuse_existing_virtualenvs = False


@nox.session(venv_backend="virtualenv", python=PYTHON_VERSION, tags=["qcheck"])
def format(session):
    """Check Python code for compliance with black formatter and imports order.

    Consider running black and isort on your code before this task.
    black --line-length 120 .
    isort --profile black  --line-length 120 .
    """
    session.log("========= format (black+isort) =========")
    session.install("black", "isort")

    session.run("black", ".", "--line-length", "120", "--check")  # Options are set in `pyproject.toml` file
    session.run(
        "isort", ".", "--line-length", "120", "--profile", "black", "--check"
    )  # Options are set in `setup.cfg` file


@nox.session(venv_backend=VENV_BACKEND, python=PYTHON_VERSION)
def qlint(session):
    """Check Python code for syntax issues."""
    session.log("============== quick lint ==============")
    session.install("flake8")
    session.run(
        "flake8",
        "--exclude=.git,__pycache__,.nox,.pytest_cache,target,.ipynb_checkpoints",
        "--select=W,E112,E113,F,C9,N8",
        "--ignore=E501,I202,F401,F841",
        "--show-source",
        "abalone",
        "tests",
        "noxfile.py",
    )


@nox.session(venv_backend=VENV_BACKEND, python=PYTHON_VERSION, tags=["qcheck"])
def lint(session):
    """Check Python code with more rules.

    Consider running black and isort on your code before lint.
    Configuration in .flake8.
    """
    session.log("================= lint =================")
    session.install(
        "flake8",
        "flake8-bandit",
        # "flake8-black",  # see format
        "flake8-bugbear",
        "flake8-docstrings",
        "darglint",
    )
    session.run(
        "flake8",
        "--exclude=.git,__pycache__,.nox,.pytest_cache,target,.ipynb_checkpoints",
        "--show-source",
        "abalone",
        "tests",
        "noxfile.py",
    )


@nox.session(venv_backend=VENV_BACKEND, python=PYTHON_VERSION)
def md_lint(session):
    """Lint markdown files.

    rules: https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md
    """
    session.log("============= markdown lint ============")
    session.install("pymarkdownlnt")
    # disable all rules checking empty lines and line length on the generated report
    session.run("pymarkdown", "--disable-rules", "MD013,MD012,MD041,MD047,MD041,MD022", "scan", "docs/report-examples")
    # ignore MD041 because of jinja comment on first line and MD013 because of long lines due to variables
    session.run("pymarkdown", "--disable-rules", "MD041,MD013", "scan", "templates")
    # all rules
    session.run("pymarkdown", "scan", "./README.md")  # TODO "docs/*.md",


@nox.session(venv_backend=VENV_BACKEND, python=PYTHON_VERSION)
def pytype(session):
    """Check types with inference - inference based."""
    session.log("================ pytype ================")
    session.install("pytype")
    # session.run("pip", "install", "--quiet", "-r", "requirements.txt")
    session.install("--quiet", "-e", ".")
    session.run("pytype", "abalone", "tests")


@nox.session(venv_backend=VENV_BACKEND, python=PYTHON_VERSION)
def mypy(session):
    """Check types - configuration in mypy.ini.

    config file documentation https://mypy.readthedocs.io/en/stable/config_file.html
    """
    session.log("================ mypy ================")
    session.install("mypy")
    # session.run("pip", "install", "--quiet", "-r", "requirements.txt")
    session.install("--quiet", "-e", ".")
    session.run(
        "mypy",
        "--install-types",
        "--non-interactive",
        "--config-file",
        ".mypy.ini",
        "--python-version",
        PYTHON_VERSION,
        "abalone",
    )
    # removed tests from the target folders as changing rules does not work


@nox.session(venv_backend=VENV_BACKEND, python=PYTHON_VERSION, tags=["qcheck"])
def unit_tests(session):
    """Run unit tests - configuration in pytest.ini."""
    session.log("============== unit tests ==============")
    session.install("pytest", "testfixtures", "coverage", "pytest-cov")
    # session.install('--quiet', '-r', 'requirements.txt')
    session.install("-e", ".")
    session.run("pytest", "--cov-report", "term", "--cov=abalone", "tests/unit")
    # TODO tags to select only tests/unit
    # TODO markers     session.run('pytest', '-m', 'fanout')


@nox.session(venv_backend=VENV_BACKEND, python=PYTHON_VERSION)
def ic_tests(session):
    """Run In-Container tests of the pipeline - configuration in pytest.ini."""
    session.log("========== in-container tests ==========")
    session.install("pytest", "testfixtures", "coverage", "pytest-cov")
    # session.install('--quiet', '-r', 'requirements.txt')
    session.install("-e", ".")
    session.run("pytest", "tests/in-container")
    # TODO gather all tests to compute coverage correctly


@nox.session(venv_backend=VENV_BACKEND, python=PYTHON_VERSION)
def create_and_run(session):
    """Define, upload and run the pipeline."""
    session.log("============ create and run ============")
    # session.install('--quiet', '-r', 'requirements.txt')
    session.install("-e", ".")
    # edited
    session.run("python", "-m", "abalone.pipeline")


@nox.session(venv_backend=VENV_BACKEND, python=PYTHON_VERSION)
def run(session):
    """Run an existing pipeline."""
    session.log("================== run =================")
    # session.install('--quiet', '-r', 'requirements.txt')
    session.install("-e", ".")
    # edited
    session.run("python", "-m", "abalone.smpipeline_runner")


@nox.session(python=PYTHON_VERSION)
def docs(session):
    """Build the documentation.

    configuration in docs/conf.py.
    template in index.rst.

    Code make use of numpy style guide
    https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard .
    """
    session.log("================ docs ================")
    session.install("sphinx")
    # session.install('--quiet', '-r', 'requirements.txt')
    session.install("--quiet", "-e", ".")
    session.run("sphinx-build", "docs/api/", "docs/api/_build")


@nox.session(python=False)
def clean(session):
    """Remove all build files and caches in the directory."""
    session.log("========== clear build items ===========")
    rmtree("build", ignore_errors=True)
    rmtree("dist", ignore_errors=True)
    rmtree("node_modules", ignore_errors=True)
    rmtree("pip-wheel-metadata", ignore_errors=True)
    # rmtree("src/" + PROJECT_NAME + ".egg-info", ignore_errors=True)
    rmtree(".egg-info", ignore_errors=True)
    rmtree(f"{PACKAGE_NAME}.egg-info", ignore_errors=True)
    rmtree(".mypy_cache", ignore_errors=True)
    rmtree(".pytest_cache", ignore_errors=True)
    session.run(
        "python3",
        "-c",
        "import pathlib;" + "[p.unlink() for p in pathlib.Path('%s').rglob('*.py[co]')]" % REPO_ROOT_PATH,
    )
    session.run(
        "python3",
        "-c",
        "import pathlib;" + "[p.rmdir() for p in pathlib.Path('%s').rglob('__pycache__')]" % REPO_ROOT_PATH,
    )


@nox.session(python=False)
def clean_runs(session):
    """Remove all files generated in the directory."""
    session.log("============ clear run items ===========")
    rmtree("generated", ignore_errors=True)
    rmtree("target", ignore_errors=True)


@nox.session(python=False)
def clean_venvs(session):
    """Remove all .venv's."""
    session.log("============== clear vens ==============")
    rmtree(".venv", ignore_errors=True)
