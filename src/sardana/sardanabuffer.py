#!/usr/bin/env python

##############################################################################
##
# This file is part of Sardana
##
# http://www.sardana-controls.org/
##
# Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
# Sardana is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# Sardana is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
##
# You should have received a copy of the GNU Lesser General Public License
# along with Sardana.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

"""This module is part Sardana Python library. It defines the base clases
for Sardana buffers"""

from __future__ import absolute_import

from taurus.external.ordereddict import OrderedDict

from sardana.sardanaevent import EventGenerator, EventType


class SardanaBuffer(EventGenerator):
    """Buffer for objects which are identified by a unique idx and are ordered
    """

    def __init__(self, objs=None, name=None, **kwargs):
        super(SardanaBuffer, self).__init__(**kwargs)
        self.name = name or self.__class__.__name__
        self._buffer = OrderedDict()
        self._next_idx = 0
        self._last_chunk = None
        if objs is not None:
            self.extend(objs)

    def get(self, idx):
        return self._buffer[idx]

    def append(self, obj, idx=None, persistent=True):
        """Append a single object at the end of the buffer with a given index.

        :param obj: object to be appened to the buffer
        :type param: object
        :param idx: at which index append obj, None means assign at the end of
            the buffer
        :type idx: int
        :param persistent: whether object should be added to a persistent
            buffer or just as a last chunk
        :type param: bool
        """
        if idx is None:
            idx = self._next_idx
        self._last_chunk = OrderedDict()
        self._last_chunk[idx] = obj
        if persistent:
            self._buffer[idx] = obj
        self._next_idx = idx + 1
        self.fire_add_event()

    def extend(self, objs, initial_idx=None, persistent=True):
        """Extend buffer with a list of objects assigning them consecutive
        indexes.

        :param objs: objects that extend the buffer
        :type param: list<object>
        :param initial_idx: at which index append the first object,
            the rest of them will be assigned the next consecutive indexes,
            None means assign at the end of the buffer
        :type idx: int
        :param persistent: whether object should be added to a persistent
            buffer or just as a last chunk
        :type param: bool
        """
        if initial_idx is None:
            initial_idx = self._next_idx
        self._last_chunk = OrderedDict()
        for idx, obj in enumerate(objs, initial_idx):
            self._last_chunk[idx] = obj
            if persistent:
                self._buffer[idx] = obj
        self._next_idx = idx + 1
        self.fire_add_event()

    def fire_add_event(self, propagate=1):
        """Fires an event to the listeners of the object which owns this
        buffer.

        :param propagate:
            0 for not propagating, 1 to propagate, 2 propagate with priority
        :type propagate: int"""
        evt_type = EventType(self.name, priority=propagate)
        self.fire_event(evt_type, self.last_chunk)

    def reset(self):

    def get_last_chunk(self):
        return self._last_chunk

    def get_next_idx(self):
        return self._next_idx

    last_chunk = property(get_last_chunk,
        doc="chunk with last value(s) added to the buffer")
    next_idx = property(get_next_idx,
        doc="index that will be automatically assigned to the next value "\
            "added to the buffer (if not explicitly assigned by the user)")
