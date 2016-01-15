===============
Getting Started
===============

.. contents::

------------
Installation
------------

streamexpect may be installed directly from `PyPi
<https://pypi.python.org/pypi/streamexpect>`__ using `pip
<https://pip.pypa.io/en/stable/>`__::

    pip install streamexpect

This will install the library as well as any dependency libraries.

The library is tested to work on the following Python versions:

* Python 2.7
* Python 3.3
* Python 3.4
* Python 3.5
* PyPy
* PyPy3


--------------------------------
The *streamexpect.wrap* Function
--------------------------------

streamexpect provides a convenience function that does much of the setup and
configuration of the streamexpect types, returning to the user an easy-to-use
wrapper over the provided stream. A common use case is communicating with a
remote socket using a simple text-based protocol. In this case, we'll use
streamexpect to talk to Google:

.. literalinclude:: ../examples/http.py
    :language: python
    :lines: 8-

streamexpect also provides intelligent support for Unicode in both Python 2
and Python 3. When using the :func:`streamexpect.wrap` function, all that is
needed to enable Unicode support is the ``unicode=True`` flag:

.. literalinclude:: ../examples/unicode.py
    :language: python
    :lines: 8-

Another common streamexpect use case is for interacting with PySerial.  Since
streamexpect does not require that the underlying stream define an actual
file, it is even possible to use streamexpect with PySerial on Windows!

.. literalinclude:: ../examples/pyserial.py
    :language: python
    :lines: 8-


---------------
Text vs. Binary
---------------

Much like Python 3, streamexpect takes a very explicit stance on what is text
and what is binary. This position carries over to streamexpect even when used
with Python 2, and therefore may catch some users unaware.

Simply stated, if a stream type returns the ``str`` type in Python 2 or the
``bytes`` type in Python 3, it is treated as a binary stream. In this case,
only binary may be provided to the :func:`Expecter.expect` method. Likewise,
if a stream type returns the ``unicode`` type in Python 2 or the ``str`` type
in Python 3, only text may be provided :func:`Expecter.expect` method.
