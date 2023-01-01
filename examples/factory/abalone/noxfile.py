# type: ignore
# This is a test file, skipping type checking in it.
"""Check code in scripts and notebooks."""
import nox

VENV_BACKEND = 'venv'

VENV_PYTHON_VERSION = '3.9'


#nox.options.sessions = ['lint', 'tests']
nox.options.sessions = ['lint', 'md_lint', 'tests']

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
            'pymarkdown', 'scan', 'templates', './README.md')


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
