import os

import setuptools

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "abalone", "__version__.py")) as f:
    exec(f.read(), about)


with open("README.md", "r") as f:
    readme = f.read()


required_packages = ["sagemaker==2.119.0", "Jinja2", "requests", "scikit-learn"]

setuptools.setup(
    name=about["__title__"],
    description=about["__description__"],
    version=about["__version__"],
    author=about["__author__"],
    author_email=["__author_email__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    url=about["__url__"],
    license=about["__license__"],
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=required_packages,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
