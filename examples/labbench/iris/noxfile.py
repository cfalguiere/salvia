# type: ignore
# This is a test file, skipping type checking in it.
"""Check code in scripts and notebooks."""
import nox

#nox.options.sessions = ['lint', 'tests']
nox.options.sessions = ['lint_notebooks', 'check_notebooks']


@nox.session(venv_backend='venv', python='3.9')
def lint_notebooks(session):
    session.install('nblint')

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


@nox.session(venv_backend='venv', python='3.9')
def check_notebooks(session):
    session.install('nbconvert')
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
