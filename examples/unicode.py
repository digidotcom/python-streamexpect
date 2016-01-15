# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2015, Digi International Inc.,  All Rights Reserved.

import io
import streamexpect

unicode_stream = io.StringIO(u'¡Se puede con español!')

with streamexpect.wrap(unicode_stream, unicode=True) as stream:
    match = stream.expect_text(u'español')
    assert match is not None
    print(u'Found {} at index {}'.format(match.match, match.start))
