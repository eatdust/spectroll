import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext
from setuptools import setup, find_packages

setup(
    name="spectroll",
    version="0.0.1",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    scripts=[],
    install_requires=['numpy'],
    package_data={'': ['data/*.dat','config.ini'],
    },

    # metadata to display on PyPI
    author="Chris Ringeval",
    author_email="eatdirt@mageia.org",
    description="Trolling from XYZ to RGB",
    license="GPLv3",
    keywords="color transformation",
    url="https://github.com/eatdust/spectroll/",   
)
