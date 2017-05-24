# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import os, sys
from setuptools.command.install import install
from setuptools.command.build import build
import tempfile
import shutil
import urllib2
import tarfile
from glob import glob
import multiprocessing
import re
import subprocessing

here = os.path.abspath(os.path.dirname(__file__))

long_description = "See website for more info."

def find_file(file_name):
    """Locate the given file from our python root."""
    for root, dirs, files in os.walk(sys.prefix):
        if file_name in files:
            return root
    
    raise Exception("Cannot find file {0}".format(file_name))

def _install_boost():

    # Extract the archive
    tar = tarfile.open(glob("*.tar.bz2")[0])
    tar.extractall()
    tar.close()

    # Find our new dir
    _, dirs, _ = next(os.walk("."))

    os.chdir(dirs[0])

    # Setup build
    try:
        subprocessing.check_output("./bootstrap.sh --prefix={0}".format(sys.prefix), shell=True)
    except Exception as e:
        raise Exception(e.output)

    # Build and install
    try:
        ret = subprocessing.check_output("./b2 install -j{0}".format(multiprocessing.cpu_count()), shell=True)
    except Exception as e:
        raise Exception(e.output)

class CustomBuildCommand(build):
    """Need to custom compile boost."""
    def run(self):
        # Save off our dir
        cwd = os.getcwd()
        self.execute(_install_boost, (), msg='Compiling/Installing z3')

        # Make sure we're in the right place
        os.chdir(cwd)
        install.run(self)

setup(
    name='larissa_boost',
    version='0.0.1',
    description='Boost library dependency building for larissa',
    long_description=long_description,
    url='https://github.com/owlz/larissa_boost',
    author='Michael Bann',
    author_email='self@bannsecurity.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Operating System :: POSIX :: Linux',
        'Environment :: Console'
    ],
    keywords='libboost',
    packages=find_packages(exclude=['contrib', 'docs', 'tests','lib']),
    cmdclass={
        'build': CustomBuildCommand,
    },
)

