# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2015 Digi International Inc. All Rights Reserved.
import ast
import re
from setuptools import setup


# Original code snippet from Flask project
# https://github.com/mitsuhiko/flask
def read_version(filename):
    regex = re.compile(r'__version__\s+=\s+(.*)')
    with open(filename, 'rb') as f:
        return str(ast.literal_eval(regex.search(
            f.read().decode('utf-8')).group(1)))


setup(
    name='streamexpect',
    version=read_version('streamexpect.py'),
    url='https://github.com/digidotcom/python-streamexpect',
    description='expect-like tools over a Python stream',
    author='Nick Stevens',
    author_email='nick.stevens@digi.com',
    keywords='expect pexpect search stream serial pyserial socket',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
    ],
    py_modules=['streamexpect'],
    install_requires=[
        'six>=1.10'
    ],
    test_suite='nose.collector',
    tests_require=[
        'testfixtures>=4.1',
    ],
    setup_requires=[
        'nose>=1.3',
        'coverage>=4.0',
        'setuptools-markdown>=0.1',
    ],
    long_description_markdown_filename='README.md',
)
