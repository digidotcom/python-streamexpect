=================
API Documentation
=================

.. contents:: Table of Contents

.. currentmodule:: streamexpect


---------
Functions
---------

.. autosummary::
    wrap

.. autofunction:: wrap


--------------
Expecter Types
--------------

.. autosummary::
    Expecter
    BytesExpecter
    TextExpecter

.. autoclass:: Expecter
   :members:

.. autoclass:: BytesExpecter
   :members:
   :inherited-members:

.. autoclass:: TextExpecter
   :members:
   :inherited-members:


--------------
Searcher Types
--------------

.. autosummary::
    Searcher
    BytesSearcher
    TextSearcher
    RegexSearcher
    SearcherCollection

.. autoclass:: Searcher
   :members:
   :private-members:

.. autoclass:: BytesSearcher
   :members:

.. autoclass:: TextSearcher
   :members:

.. autoclass:: RegexSearcher
   :members:

.. autoclass:: SearcherCollection
   :members:


-----------
Match types
-----------

.. autosummary::
    SequenceMatch
    RegexMatch

.. autoclass:: SequenceMatch
   :members:

.. autoclass:: RegexMatch
   :members:


-------------------
StreamAdapter Types
-------------------

.. autosummary::
    StreamAdapter
    PollingStreamAdapter
    PollingSocketStreamAdapter
    PollingStreamAdapterMixin

.. autoclass:: StreamAdapter
   :members:

.. autoclass:: PollingStreamAdapter
   :members:

.. autoclass:: PollingSocketStreamAdapter
   :members:

.. autoclass:: PollingStreamAdapterMixin
   :members:


----------
Exceptions
----------

.. autosummary::
   ExpectTimeout

.. autoclass:: ExpectTimeout
   :members:
