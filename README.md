streamexpect
============

[![Build Status](https://travis-ci.org/digidotcom/python-streamexpect.svg?branch=master)](https://travis-ci.org/digidotcom/python-streamexpect)
[![Coverage Status](https://img.shields.io/coveralls/digidotcom/python-streamexpect.svg)](https://coveralls.io/r/digidotcom/python-streamexpect)
[![Code Climate](https://img.shields.io/codeclimate/github/digidotcom/python-streamexpect.svg)](https://codeclimate.com/github/digidotcom/python-streamexpect)
[![GitHub Issues](https://img.shields.io/github/issues/digidotcom/python-streamexpect.svg)](https://github.com/digidotcom/python-streamexpect/issues)
[![PyPI](https://img.shields.io/pypi/v/streamexpect.svg)](https://pypi.python.org/pypi/streamexpect/)
[![License](https://img.shields.io/badge/license-MPL%202.0-blue.svg)](https://github.com/digidotcom/python-streamexpect/blob/master/LICENSE.txt)

streamexpect is a library providing cross-platform "expect-like" functionality
for generic Python streams and sockets . It is similar to the
[Pexpect](https://pexpect.readthedocs.org) library, except where Pexpect
explicitly requires an underlying file (usually a TTY), streamexpect uses
duck-typing and requires only a `read` or `recv` method.

[View the Full Documentation](https://digidotcom.github.io/python-streamexpect)

The original version of streamexpect was generously donated by
[Digi](http://www.digi.com) [Wireless Design Services](http://www.digi.com/wds).
The software is provided as Alpha software and has not undergone formal
testing. It does, however, ship with extensive unit testing.

[View the Changelog](https://github.com/digidotcom/python-streamexpect/blob/master/CHANGELOG.md)

Installation
============

Installation is performed using pip. The latest released version of
streamexpect can be obtained with the following command:

```sh
$ pip install streamexpect
```

To install the development version from GitHub:

```sh
$ pip install -U -e 'git+https://github.com/digidotcom/python-streamexpect#egg=streamexpect'
```

Example
=======

The following example shows opening a serial port (on a Windows PC), sending
the `uname` command, and verifying that _Linux_ is in the returned data.

```python
import serial
import streamexpect

# timeout=0 is essential, as streams are required to be non-blocking
ser = serial.Serial('COM1', baudrate=115200, timeout=0)

with streamexpect.wrap(ser) as stream:
  stream.write('\r\nuname -a\r\n')
  match = stream.expect_bytes('Linux', timeout=1.0)
  print(u'Found Linux at index {}'.format(match.start))
```


Design Goals
============

* Be Cross-Platform

  The library should not depend on any features (besides Python) that exclude a
  platform. Yes, that means Windows is a first-class citizen.

* Be Explicit In Encoding

  When dealing with streams of data, the distinction between when the stream
  goes from being a series of binary bytes to a set of encoded characters can
  be unclear. The library should be explicit in the handling of binary versus
  characters, such that mixing the two types is not allowed without explicit
  options to enable encoding and decoding.

* Common Use Cases Should Be Simple

  For 95% of users, the `streamexpect.wrap` function should accomplish the
  desired goals. Intelligent default options should be used so the library just
  "does the right thing".

* Complicated Use Cases Should Be Possible

  The objects returned by the `streamexpect.wrap` function should themselves be
  easy to use and extend. Protocol requirements between classes should be
  explicit and documented.


Development
===========

Development of streamexpect takes place in the open on GitHub. Please use pull
requests to submit changes to code and documentation.

The process for building and testing streamexpect has been automated as much as
possible. [tox](https://testrun.org/tox/) handles building and testing the
code, as well as generating documentation and automatically testing for code
style issues. tox can be installed with pip:

    pip install tox

The generic tox command looks like:

    tox

This will attempt to build and test streamexpect against multiple different
versions of Python, and will error on versions not found. To test against only
a single version of Python, specify the version at the tox command line. For
example, to test only Python 2.7:

    tox -e py27

Multiple versions may be specified, separated by a comma:

    tox -e py27,py35

Documentation generation and code style checking are not performed by default,
and so must be explicitly provided to the tox command. Documentation generation
requires either Python 2.7, or Python 3.3 or greater.

    tox -e docs,style


License
=======

This software is open-source software. Copyright Digi International, 2015.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
you can obtain one at http://mozilla.org/MPL/2.0/.
