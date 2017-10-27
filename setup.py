import os.path
import pip
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

import factoryfactory
version = factoryfactory.VERSION


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main([self.pytest_args])
        sys.exit(errno)


setup(
    name='factoryfactory',
    packages=['factoryfactory'],
    version=version,
    description='A simple service locator in Python',
    author='James McKay',
    author_email='code@jamesmckay.net',
    keywords=['service-location', 'inversion-of-control', 'ioc'],
    url='https://github.com/jammycakes/factoryfactory',
    download_url = 'https://github.com/jammycakes/factoryfactory/archive/{0}.tar.gz'.format(version),
    license='MIT',
    install_requires=[],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},
)