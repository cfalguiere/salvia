Conversation: Scaff nox

---

# You are a professional Python developper.  Yu build your projects using nox, the Pythonn automation tool.

Instructions are given in a configuration file named  noxfile.py 

Here is an example of such a file.

# import nox
import nox

# set python version to 3.8
PYTHON_VERSION = "3.8"

# prevent from reusing virtualenvs
nox.options.reuse_existing_virtualenvs = False

# define the list of sessions
nox.options.sessions = ["lint"]
#nox.options.sessions = ["format", "lint", "md_lint", "mypy", "unit_tests", "docs"]

# lint the code 
@nox.session(venv_backend=VENV_BACKEND, python=PYTHON_VERSION)
def qlint(session):
    """Check Python code for syntax issues."""
    session.log("============== quick lint ==============")
    session.install("flake8")
    session.run(
        "flake8",
        "--exclude=env,.git,__pycache__,.nox,.pytest_cache,target,.ipynb_checkpoints",
        "--select=W,E112,E113,F,C9,N8",
        "--ignore=E501,I202,F401,F841",
        "--show-source",
        "."
    )


Do not output the file now. I will provide more instructions to write the file.

---

Write a noxfile using the following information:
- python version is 3.7 
- allow to reuse virtual envs
- run the following sessions: lint

NOTES:
- correct