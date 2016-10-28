# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2015 Digi International Inc. All Rights Reserved.

import io
import re
import six
import streamexpect
import socket
import sys
import testfixtures
import unittest

from six import u

from streamexpect import BytesSearcher
from streamexpect import Expecter
from streamexpect import ExpectTimeout
from streamexpect import PollingSocketStreamAdapter
from streamexpect import PollingStreamAdapter
from streamexpect import RegexMatch
from streamexpect import RegexSearcher
from streamexpect import Searcher
from streamexpect import SearcherCollection
from streamexpect import SequenceMatch
from streamexpect import StreamAdapter
from streamexpect import TextSearcher


class TestSequenceMatch(unittest.TestCase):

    def test_repr(self):
        # Only check no exceptions thrown
        match = SequenceMatch(TextSearcher(u('rho')), 'rho', 0, 3)
        repr(match)


class TestRegexMatch(unittest.TestCase):

    def test_repr(self):
        # Only check no exceptions thrown
        match = RegexMatch(RegexSearcher(u('rho')), 'rho', 0, 3, None)
        repr(match)


class PiecewiseStream(io.RawIOBase):

    def __init__(self, string, max_chunk=None):
        self.max_chunk = max_chunk or sys.maxsize
        self.string = string
        self.idx = 0

    def read(self, n):
        if self.idx >= len(self.string):
            return ''
        else:
            take = min(n, self.max_chunk)
            chunk = self.string[self.idx:self.idx+take]
            self.idx += len(chunk)
            return chunk


class EmptyStream(io.RawIOBase):

    def read(self, n):
        return ''


class SearcherTest(unittest.TestCase):

    def setUp(self):
        self.searcher = Searcher()

    def test_repr(self):
        # Only check no exceptions thrown
        repr(self.searcher)

    def test_search(self):
        with self.assertRaises(NotImplementedError):
            self.searcher.search('')

    def test_match_type(self):
        with self.assertRaises(NotImplementedError):
            self.searcher.match_type

    def test_match_type_read_only(self):
        with self.assertRaises(AttributeError):
            self.searcher.match_type = 'foobar'


class TestTextSearcher(unittest.TestCase):

    def test_text_constructor(self):
        searcher = TextSearcher(u('some unicode'))
        self.assertEqual(searcher.match_type, six.text_type)

    def test_fail_using_bytes(self):
        with self.assertRaises(TypeError):
            TextSearcher(b'bytes type')

    def test_not_patterns(self):
        with self.assertRaises(TypeError):
            TextSearcher(None)
        with self.assertRaises(TypeError):
            TextSearcher(5)

    def test_no_match(self):
        uut = TextSearcher(u('I will never match'))
        self.assertEqual(None, uut.search(u('alpha beta gamma')))

    def test_single_match(self):
        uut = TextSearcher(u('one'))
        match = uut.search(u('the number one appears once'))
        self.assertIsNotNone(match)
        self.assertEqual(11, match.start)
        self.assertEqual(14, match.end)

    def test_multi_match(self):
        uut = TextSearcher(u('one'))
        match = uut.search(u('one two three two one'))
        self.assertIsNotNone(match)
        self.assertEqual(0, match.start)
        self.assertEqual(3, match.end)

    def test_unicode_combining_characters(self):
        # Some unicode characters can be represented in multiple ways - for
        # example, an accented character may be a single code point (with the
        # accent baked in), or it may be the "normal" letter with a combining
        # code point. See https://docs.python.org/2/library/unicodedata.html.
        # The points below are for a capital C with a cedilla, first as a
        # composite character, second as a pairing of C and the cedilla
        # combining character.
        composite = six.unichr(0xC7)
        combining = six.unichr(0x43) + six.unichr(0x0327)

        # Test combinations of search and character
        for text in composite, combining:
            searcher = TextSearcher(text)
            self.assertIsNotNone(searcher.search(composite))
            self.assertIsNotNone(searcher.search(combining))

    def test_repr(self):
        # Only check no exceptions thrown
        searcher = TextSearcher(u('rho'))
        repr(searcher)


class TestBytesSearcher(unittest.TestCase):

    def test_binary_constructor(self):
        searcher = BytesSearcher(b'\x01\x02\x03\x04')
        self.assertEqual(searcher.match_type, six.binary_type)

    def test_fail_using_text(self):
        with self.assertRaises(TypeError):
            BytesSearcher(u('I am Unicode text'))

    def test_not_patterns(self):
        with self.assertRaises(TypeError):
            BytesSearcher(None)
        with self.assertRaises(TypeError):
            BytesSearcher(5)

    def test_no_match(self):
        uut = BytesSearcher(b'I will never match')
        self.assertEqual(None, uut.search(b'alpha beta gamma'))

    def test_single_match(self):
        uut = BytesSearcher(b'\x05\x05')
        match = uut.search(b'ascii with \x05\x05 bytes')
        self.assertIsNotNone(match)
        self.assertEqual(11, match.start)
        self.assertEqual(13, match.end)

    def test_multi_match(self):
        uut = BytesSearcher(b'one')
        match = uut.search(b'one two three two one')
        self.assertIsNotNone(match)
        self.assertEqual(0, match.start)
        self.assertEqual(3, match.end)

    def test_repr(self):
        # Only check no exceptions thrown
        searcher = BytesSearcher(b'\x00\x00')
        repr(searcher)


class TestRegexSearcher(unittest.TestCase):

    def test_constructor_text_pattern(self):
        searcher = RegexSearcher(u('Unicode pattern'))
        self.assertEqual(searcher.match_type, six.text_type)
        searcher = RegexSearcher(b'ASCII pattern')
        self.assertEqual(searcher.match_type, six.binary_type)
        searcher = RegexSearcher(re.compile(u('Unicode precompiled')))
        self.assertEqual(searcher.match_type, six.text_type)
        searcher = RegexSearcher(re.compile(b'ASCII precompiled'))
        self.assertEqual(searcher.match_type, six.binary_type)

    def test_no_patterns(self):
        with self.assertRaises(TypeError):
            RegexSearcher(None)
        with self.assertRaises(TypeError):
            RegexSearcher(5)

    def test_text(self):
        uut = RegexSearcher(u('omicron'))
        match = uut.search(u('omicron pi rho'))
        self.assertIsNotNone(match)
        self.assertEqual(0, match.start)
        self.assertEqual(7, match.end)

    def test_binary(self):
        uut = RegexSearcher(b'omicron')
        match = uut.search(b'omicron pi rho')
        self.assertIsNotNone(match)
        self.assertEqual(0, match.start)
        self.assertEqual(7, match.end)

    def test_mismatched_types(self):
        text_searcher = RegexSearcher(u('omicron'))
        with self.assertRaises(TypeError):
            text_searcher.search(b'omicron')
        binary_searcher = RegexSearcher(b'omicron')
        with self.assertRaises(TypeError):
            binary_searcher.search(u('omicron'))

    def test_single_regex_multi_match(self):
        uut = RegexSearcher('omicron')
        match = uut.search('pi delta omicron rho omicron')
        self.assertIsNotNone(match)
        self.assertEqual(9, match.start)
        self.assertEqual(16, match.end)

    def test_repr(self):
        # Only check no exceptions thrown
        searcher = RegexSearcher('[eu]psilon')
        repr(searcher)


class TestSearcherCollection(unittest.TestCase):

    def test_constructor(self):
        s1, s2 = TextSearcher(u('')), TextSearcher(u(''))
        searcher = SearcherCollection(s1, s2)
        self.assertEqual(six.text_type, searcher.match_type)
        self.assertEqual([s1, s2], list(searcher))
        searcher = SearcherCollection([s1, s2])
        self.assertEqual(six.text_type, searcher.match_type)
        self.assertEqual([s1, s2], list(searcher))
        searcher = SearcherCollection(s1)
        self.assertEqual([s1], list(searcher))
        self.assertEqual(six.text_type, searcher.match_type)

    def test_constructor_invalid(self):
        with self.assertRaises(ValueError):
            SearcherCollection([])
        with self.assertRaises(TypeError):
            SearcherCollection(1)
        with self.assertRaises(ValueError):
            SearcherCollection(TextSearcher(u('')), BytesSearcher(b''))

        NoSearchSearcher = type('NoSearchSearcher', (object,),
                                {'match_type': None})
        with self.assertRaises(TypeError):
            SearcherCollection(NoSearchSearcher())

        NoMatchTypeSearcher = type('NoMatchTypeSearcher', (object,),
                                   {'search': None})
        with self.assertRaises(TypeError):
            SearcherCollection(NoMatchTypeSearcher())

    def test_multi_regex_single_match(self):
        uut = SearcherCollection([
            RegexSearcher('omicron'),
            RegexSearcher('[eu]psilon'),
        ])
        match = uut.search('pi epsilon iota rho')
        self.assertIsNotNone(match)
        self.assertEqual(1, uut.index(match.searcher))
        self.assertEqual(3, match.start)
        self.assertEqual(10, match.end)

    def test_multi_regex_multi_match(self):
        uut = SearcherCollection([
            RegexSearcher(u('omicron')),
            RegexSearcher(u('[eu]psilon')),
            TextSearcher(u('pi')),
            TextSearcher(u('iota')),
        ])
        match = uut.search(u('pi iota epsilon upsilon omicron'))
        self.assertIsNotNone(match)
        self.assertEqual(2, uut.index(match.searcher))
        self.assertEqual(0, match.start)
        self.assertEqual(2, match.end)

    def test_search_wrong_type(self):
        uut = SearcherCollection([
            RegexSearcher(b'omicron'),
            RegexSearcher(b'[eu]psilon'),
        ])
        with self.assertRaises(TypeError):
            uut.search(u('pi omicron mu'))

    def test_repr(self):
        # Only check no exceptions thrown
        searcher = SearcherCollection([TextSearcher(u('epsilon')),
                                       RegexSearcher(u('[eu]psilon'))])
        repr(searcher)


class TestStreamAdapter(unittest.TestCase):

    def test_constructor(self):
        with self.assertRaises(NotImplementedError):
            StreamAdapter(None).poll(10)

    def test_delegation(self):
        stream = io.StringIO(u('hello'))
        adapter = StreamAdapter(stream)
        self.assertEqual('hello', adapter.getvalue())

    def test_repr(self):
        # Only check no exceptions thrown
        adapter = StreamAdapter(None)
        repr(adapter)


class TestPollingStreamAdapter(unittest.TestCase):

    def test_constructor(self):
        stream = io.StringIO()
        adapter = PollingStreamAdapter(stream, poll_period=1, max_read=32)
        self.assertEqual(1, adapter.poll_period)
        self.assertEqual(32, adapter.max_read)

    def test_bad_property_values(self):
        stream = io.StringIO()
        adapter = PollingStreamAdapter(stream, poll_period=1, max_read=32)
        with self.assertRaises(ValueError):
            adapter.poll_period = 0
        with self.assertRaises(ValueError):
            adapter.max_read = -1

    def test_poll(self):
        stream = PiecewiseStream(b'alpha beta gamma omega', max_chunk=5)
        with testfixtures.Replacer() as r:
            mock_time = testfixtures.test_time(delta=0.1, delta_type='seconds')
            r.replace('streamexpect.time.time', mock_time)
            adapter = PollingStreamAdapter(stream)
            for chunk in (b'alpha', b' beta', b' gamm', b'a ome'):
                self.assertEqual(chunk, adapter.poll(1.0))

    def test_timeout(self):
        with testfixtures.Replacer() as r:
            mock_time = testfixtures.test_time(delta=0.1, delta_type='seconds')
            r.replace('streamexpect.time.time', mock_time)
            r.replace('streamexpect.time.sleep', lambda _: None)
            stream = EmptyStream()
            adapter = PollingStreamAdapter(stream)
            with self.assertRaises(ExpectTimeout):
                adapter.poll(1)


class TestPollingSocketStreamAdapter(unittest.TestCase):

    def test_constructor(self):
        sock = socket.socket()
        try:
            adapter = PollingSocketStreamAdapter(sock, poll_period=1,
                                                 max_read=32)
            self.assertEqual(1, adapter.poll_period)
            self.assertEqual(32, adapter.max_read)
        finally:
            sock.close()

    def test_bad_property_values(self):
        sock = socket.socket()
        adapter = PollingSocketStreamAdapter(sock, poll_period=1, max_read=32)
        with self.assertRaises(ValueError):
            adapter.poll_period = 0
        with self.assertRaises(ValueError):
            adapter.max_read = -1
        sock.close()

    def test_poll(self):
        source, drain = socket.socketpair()
        try:
            with testfixtures.Replacer() as r:
                mock_time = testfixtures.test_time(delta=0.1,
                                                   delta_type='seconds')
                r.replace('streamexpect.time.time', mock_time)
                adapter = PollingSocketStreamAdapter(drain)
                for chunk in (b'alpha', b' beta', b' gamm', b'a ome'):
                    source.send(chunk)
                    self.assertEqual(chunk, adapter.poll(1.0))
        finally:
            source.close()
            drain.close()

    def test_timeout(self):
        source, drain = socket.socketpair()
        try:
            with testfixtures.Replacer() as r:
                mock_time = testfixtures.test_time(delta=0.1,
                                                   delta_type='seconds')
                r.replace('streamexpect.time.time', mock_time)
                adapter = PollingSocketStreamAdapter(drain)
                with self.assertRaises(ExpectTimeout):
                    adapter.poll(0.01)
        finally:
            source.close()
            drain.close()


class TestExpecter(unittest.TestCase):

    class NoPollMethod(object):
        pass

    def test_constructor(self):
        adapter = PollingStreamAdapter(PiecewiseStream(u('')))
        expecter = Expecter(adapter, input_callback=None, window=1024,
                            close_adapter=False)
        self.assertEqual(1024, expecter.window)
        self.assertTrue(expecter.stream_adapter is adapter)
        self.assertEqual('', expecter.read(10))
        self.assertFalse(expecter.close_adapter)

    def test_bad_attributes(self):
        adapter = PollingStreamAdapter(PiecewiseStream(u('tau iota mu')))
        with self.assertRaises(TypeError):
            Expecter(adapter, input_callback=None, window=None,
                     close_adapter=False)
        with self.assertRaises(ValueError):
            Expecter(adapter, input_callback=None, window=-22,
                     close_adapter=False)
        with self.assertRaises(NotImplementedError):
            Expecter(adapter, input_callback=None, window=1024,
                     close_adapter=False).expect(None, 0)
        with self.assertRaises(TypeError):
            Expecter(TestExpecter.NoPollMethod(), input_callback=None,
                     window=1024, close_adapter=False)


class TestWrapper(unittest.TestCase):

    def test_expect_bytes(self):
        source, drain = socket.socketpair()
        try:
            wrapper = streamexpect.wrap(drain, unicode=False)
            source.sendall(b'tau iota mu')
            match = wrapper.expect_bytes(b'iota')
            self.assertTrue(match is not None)
            self.assertEqual(b'iota', match.match)
        finally:
            source.close()
            drain.close()

    def test_expect_text(self):
        stream = PiecewiseStream(u('tau iota mu'), max_chunk=3)
        wrapper = streamexpect.wrap(stream, unicode=True)
        match = wrapper.expect_text(u('iota'))
        self.assertTrue(match is not None)
        self.assertEqual(u('iota'), match.match)

    def test_expect_bytes_twice_on_one_buffer(self):
        source, drain = socket.socketpair()
        try:
            wrapper = streamexpect.wrap(drain, unicode=False)
            source.sendall(b'tau iota mu')
            match = wrapper.expect_bytes(b'iota')
            self.assertTrue(match is not None)
            self.assertEqual(b'iota', match.match)
            match = wrapper.expect_bytes(b'mu')
            self.assertTrue(match is not None)
            self.assertEqual(b'mu', match.match)
        finally:
            source.close()
            drain.close()

    def test_expect_bytes_twice_on_split_buffer_with_small_window(self):
        source, drain = socket.socketpair()
        try:
            wrapper = streamexpect.wrap(drain, unicode=False, window=8)
            source.sendall(b'tau iota m')
            match = wrapper.expect_bytes(b'iota')
            self.assertTrue(match is not None)
            self.assertEqual(b'iota', match.match)
            source.sendall(b'u tau iota')
            match = wrapper.expect_bytes(b'mu')
            self.assertTrue(match is not None)
            self.assertEqual(b'mu', match.match)
        finally:
            source.close()
            drain.close()

    def test_expect_text_twice(self):
        stream = PiecewiseStream(u('tau iota mu'), max_chunk=3)
        wrapper = streamexpect.wrap(stream, unicode=True)
        match = wrapper.expect_text(u('iota'))
        self.assertTrue(match is not None)
        self.assertEqual(u('iota'), match.match)
        match = wrapper.expect_text(u('mu'))
        self.assertTrue(match is not None)
        self.assertEqual(u('mu'), match.match)

    def test_expect_text_twice_with_small_window(self):
        stream = PiecewiseStream(u('tau iota epsilon mu'), max_chunk=20)
        wrapper = streamexpect.wrap(stream, unicode=True, window=8)
        match = wrapper.expect_text(u('iota'))
        self.assertTrue(match is not None)
        self.assertEqual(u('iota'), match.match)
        match = wrapper.expect_text(u('mu'))
        self.assertTrue(match is not None)
        self.assertEqual(u('mu'), match.match)
        
    def test_expect_unicode_regex(self):
        stream = PiecewiseStream(u('pi epsilon mu'), max_chunk=3)
        wrapper = streamexpect.wrap(stream, unicode=True)
        match = wrapper.expect_regex(u('[eu]psilon'))
        self.assertTrue(match is not None)
        self.assertEqual(u('epsilon'), match.match)

    def test_echo_bytes(self):
        stream = PiecewiseStream(b'pi epsilon mu')
        wrapper = streamexpect.wrap(stream, unicode=False, echo=True)
        with testfixtures.OutputCapture() as output:
            match = wrapper.expect_regex(b'[eu]psilon')
            output.compare('pi epsilon mu')
            self.assertTrue(match is not None)
            self.assertEqual(b'epsilon', match.match)

    def test_echo_text(self):
        stream = PiecewiseStream(u('pi epsilon mu'))
        wrapper = streamexpect.wrap(stream, unicode=True, echo=True)
        with testfixtures.OutputCapture() as output:
            match = wrapper.expect_regex(u('[eu]psilon'))
            output.compare('pi epsilon mu')
            self.assertTrue(match is not None)
            self.assertEqual(u('epsilon'), match.match)

    def test_context_manager(self):
        stream = EmptyStream()
        with streamexpect.wrap(stream, close_stream=True):
            pass
        self.assertTrue(stream.closed)

    def test_context_manager_no_close_stream(self):
        stream = EmptyStream()
        with streamexpect.wrap(stream, close_stream=False):
            pass
        self.assertFalse(stream.closed)

    def test_unhandled_type(self):
        with self.assertRaises(TypeError):
            streamexpect.wrap(b'')
