============
streamexpect
============

Version: |version|

streamexpect is a library providing cross-platform "expect-like" functionality
for generic Python streams and sockets . It is similar to the `Pexpect
<https://pexpect.readthedocs.org>`__ library, except where Pexpect explicitly
requires an underlying file (usually a TTY), streamexpect uses duck-typing and
requires only a `read` or `recv` method.

.. toctree::
   :maxdepth: 2

   getting_started
   api
