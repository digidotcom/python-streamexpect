# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2015, Digi International Inc.,  All Rights Reserved.

import socket
import streamexpect

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('www.google.com', 80))

# By default, this will open in binary mode. To read a non-ASCII text stream,
# the unicode option needs to be enabled.
with streamexpect.wrap(sock) as stream:

    # Send the request. This is passed to the underlying socket.
    stream.sendall(b'GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n')

    # Find the start of the response.
    stream.expect_bytes(b'HTTP/1.1 200 OK\r\n')

    # Find the "Date" header using regex groups and print it.
    match = stream.expect_regex(br'Date: ([^\r\n]+)\r\n')
    print(u'Google says the date/time is ' + match.groups[0].decode('ascii'))
