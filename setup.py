#!/usr/bin/env python
from codecs import open
from os import path
from os import linesep

import subprocess

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

here = path.abspath(path.dirname(__file__))


def readme():
    with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

    return long_description


def git_version():
    # Fetch version from git tags, and write to version.py.
    # Also, when git is not available (PyPi package), use storedversion.py.
    version_py = path.join(here, 'craftai', 'version.py')

    try:
        version_git = (
            subprocess.check_output(
                ["git", "describe", "--tags"]
            ).rstrip()).decode("utf-8")
    except:
        with open(version_py, 'r') as fh:
            version_git = (
                fh.read().
                strip().split('=')[-1].replace('"', ''))

    version_msg = ("""# Do not edit this file, pipeline versioning is"""
                   """ governed by git tags.""")

    with open(version_py, 'w') as fh:
        fh.write(version_msg + linesep + "__version__=" + version_git)

    return version_git

setup(
    name='craft-ai',

    version=git_version(),

    description='craft ai API client for python',
    long_description=readme(),

    author='craft.ai team',
    author_email='contact@craft.ai',
    url='https://github.com/craft-ai/craft-ai-client-python/',

    # Choose your license
    license='BSD 3-Clause',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',

        # Should match "license" above)
        'License :: OSI Approved :: BSD License',

        # Python versions against which the code has been tested and is
        # actively supported.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='ai craft-ai',

    packages=['craftai'],
    install_requires=[
        'requests',
        'six',
        'datetime',
        'pytz',
        'tzlocal',
        'pypandoc'
    ],

    extras_require={
        'dev': ['python-dotenv'],
        'test': ['tox', 'nose'],
    },

    include_package_data=True,
    entry_points={
        'console_scripts': [
            'craft-ai= craftai.cli:main'
        ]
    }
)
