"""setup.py.

Set up details for ``pip install ising_sim`` or ``pip install -e .`` if
installing by source.

"""

import setuptools
from ising_sim import __version__, __name__


with open('README.rst') as f:
    README = f.read()

with open("requirements.txt") as f:
    REQUIREMENTS = [line.strip() for line in f if line.strip()]


setuptools.setup(
    name=__name__,
    version=__version__,
    author="Joseph T. Iosue",
    author_email="joe.iosue@yahoo.com",
    description="A package for simulating a 1D spin chain with or without GUI",
    long_description=README,
    long_description_content_type='text/x-rst',
    url="https://github.com/jiosue/ising_sim",
    license="MIT License",
    packages=setuptools.find_packages(exclude=("tests", "docs")),
    install_requires=REQUIREMENTS,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Source": "https://github.com/jiosue/ising_sim",
    }
)
