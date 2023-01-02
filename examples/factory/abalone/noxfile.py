# type: ignore
# This is a test file, skipping type checking in it.
"""Check code in scripts and notebooks."""
import nox

from os.path import abspath, dirname
from shutil import rmtree


PROJECT_NAME = "abalone"
PACKAGE_NAME = "abalone"
REPO_ROOT_PATH = dirname(abspath(__file__))

VENV_BACKEND = 'venv'

VENV_PYTHON_VERSION = '3.9'

nox.options.stop_on_first_error = True

#nox.options.sessions = ['lint', 'tests']
nox.options.sessions = ['lint', 'md_lint', 'tests']

nox.options.envdir = ".venv"
#nox.options.reuse_existing_virtualenvs = True
nox.options.reuse_existing_virtualenvs = False


@nox.session(venv_backend=VENV_BACKEND, python=VENV_PYTHON_VERSION)
def tests(session):
    session.install('pytest', 'testfixtures', 'coverage', 'pytest-cov')
    #session.install('--quiet', '-r', 'requirements.txt')
    session.install('-e', '.')
    session.run('pytest', '--cov-report', 'term', '--cov=abalone', 'tests/unit')
    # TODO select only tests/unit


@nox.session(venv_backend='venv', python='3.9')
def lint(session):
    session.install('flake8')
    session.run(
            'flake8',
            '--exclude=.git,__pycache__,.nox,.pytest_cache,target,.ipynb_checkpoints',
            '--select=W,E112,E113,F,C9,N8',
            '--ignore=E501,I202,F401,F841',
            '--show-source',
            'abalone', 'tests/unit', 'noxfile.py')


@nox.session(venv_backend='venv', python='3.9')
def md_lint(session):
    session.install('pymarkdownlnt')
    session.run(
            'pymarkdown', '--disable-rules', 'MD013', 'scan', 'templates', './README.md')


@nox.session(venv_backend='venv', python='3.9')
def run(session):
    #session.install('--quiet', '-r', 'requirements.txt')
    session.install('-e', '.')
    # edited
    session.run('python', '-m', 'abalone.pipeline')


@nox.session(venv_backend='venv', python='3.9')
def exec(session):
    #session.install('--quiet', '-r', 'requirements.txt')
    session.install('-e', '.')
    # edited
    session.run('python', '-m', 'abalone.smpipeline_runner')



@nox.session(python=False)
def clean(session):
    """Remove all build files and caches in the directory."""
    rmtree("build", ignore_errors=True)
    rmtree("dist", ignore_errors=True)
    rmtree("node_modules", ignore_errors=True)
    rmtree("pip-wheel-metadata", ignore_errors=True)
    #rmtree("src/" + PROJECT_NAME + ".egg-info", ignore_errors=True)
    rmtree(".egg-info", ignore_errors=True)
    rmtree(".mypy_cache", ignore_errors=True)
    rmtree(".pytest_cache", ignore_errors=True)
    session.run(
        "python3",
        "-c",
        "import pathlib;"
        + "[p.unlink() for p in pathlib.Path('%s').rglob('*.py[co]')]"
        % REPO_ROOT_PATH,
    )
    session.run(
        "python3",
        "-c",
        "import pathlib;"
        + "[p.rmdir() for p in pathlib.Path('%s').rglob('__pycache__')]"
        % REPO_ROOT_PATH,
    )
    

@nox.session(python=False)
def clean_venvs(session):
    """Remove all .venv's."""
    rmtree(".venv", ignore_errors=True)
