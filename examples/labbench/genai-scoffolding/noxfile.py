import nox

# Set Python version to 3.7
PYTHON_VERSION = "3.7"

# Allow reusing virtual environments
nox.options.reuse_existing_virtualenvs = True

# Define the list of sessions
nox.options.sessions = ["lint", "unit_tests"]

# Lint the code
@nox.session(python=PYTHON_VERSION)
def lint(session):
    """Check Python code for syntax issues."""
    session.log("============== Linting ==============")
    session.install("flake8")
    session.run(
        "flake8",
        "--exclude=env,.git,__pycache__,.nox,.pytest_cache,target,.ipynb_checkpoints",
        "--select=W,E112,E113,F,C9,N8",
        "--ignore=E501,I202,F401,F841",
        "--show-source",
        "."
    )

# not chatgpt
# test the code
@nox.session(python=PYTHON_VERSION)
def unit_tests(session):
    """Run unit tests - configuration in pytest.ini."""
    session.log("============== unit tests ==============")
    session.install('--quiet', "pytest", "testfixtures")
    # session.install('--quiet', '-r', 'requirements.txt')
    session.install("-e", ".")
    session.run("pytest",  "tests")
