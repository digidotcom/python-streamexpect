# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2015, Digi International Inc.,  All Rights Reserved.

# Send the uname command to a Linux PC connected to a Windows PC over serial
import serial
import streamexpect

# timeout=0 is essential, as streams are required to be non-blocking
ser = serial.Serial('COM1', baudrate=115200, timeout=0)

with streamexpect.wrap(ser) as stream:
    stream.write(b'\r\nuname -a\r\n')
    match = stream.expect_bytes(b'Linux', timeout=1.0)
    print(u'Found Linux at index {}'.format(match.start))
