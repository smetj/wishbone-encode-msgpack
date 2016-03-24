#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  msgpackencode.py
#
#  Copyright 2016 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from wishbone import Actor
import msgpack


class MSGPackEncode(Actor):
    '''
    **Converts Python dict data structures to MSGPack format.**

    Parameters:

        - complete(bool)(False)
           |  When True encodes the complete event.  If False only
           |  encodes the data part.

    Queues:

        - inbox
           |  Incoming messages

        - outbox
           |  Outgoing messges
    '''

    def __init__(self, actor_config, complete=False):
        Actor.__init__(self, actor_config)

        self.pool.createQueue("inbox")
        self.pool.createQueue("outbox")

        self.registerConsumer(self.consume, "inbox")

    def preHook(self):

        if self.kwargs.complete:
            self.encode = self.__encodeComplete
        else:
            self.encode = self.__encodeData

    def consume(self, event):
        event.set(self.encode(event))
        self.submit(event, self.pool.queue.outbox)

    def __encodeComplete(self, event):
        return msgpack.packb(event.dump(convert_timestamp=False))

    def __encodeData(self, event):
        return msgpack.packb(event.get())
