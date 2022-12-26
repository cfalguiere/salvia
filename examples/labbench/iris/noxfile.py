# type: ignore
# This is a test file, skipping type checking in it.
"""Check code in scripts and notebooks."""
import nox


VENV_BACKEND = 'venv'

VENV_PYTHON_VERSION = '3.9'

nox.options.sessions = ['nblint']


@nox.session(venv_backend=VENV_BACKEND, python=VENV_PYTHON_VERSION)
def nblint(session):
    session.install('nblint')
    session.install('sagemaker==2.120.0')

    import os
    for root, dirs, files in os.walk('./notebooks/'):
        if 'output' not in root:
            for name in files:
                if name.endswith('.ipynb'):
                    if 'checkpoint' not in name:
                        filename = os.path.join(root, name)
                        session.run(
                                'nblint',
                                '--linter',
                                'pyflakes',
                                filename)
    # TODO ignore magic


@nox.session(venv_backend=VENV_BACKEND, python=VENV_PYTHON_VERSION)
def nbcheck(session):
    session.install('nbconvert')
    session.install('sagemaker==2.120.0')
    import os
    for root, dirs, files in os.walk('./notebooks/'):
        if 'output' not in root:
            for name in files:
                if name.endswith('.ipynb'):
                    if 'checkpoint' not in name:
                        filename = os.path.join(root, name)
                        session.run(
                                'jupyter',
                                'nbconvert',
                                '--to',
                                'notebook',
                                '--execute',
                                '--output',
                                'check',
                                filename)
