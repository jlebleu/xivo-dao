# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from xivo_dao.helpers.abstract_model import AbstractModels


class Line(AbstractModels):

    MANDATORY = [
        'name',
        'context',
        'protocol'
    ]

    # mapping = {db_field: model_field}
    _MAPPING = {
        'id': 'id',
        'name': 'name',
        'number': 'number',
        'context': 'context',
        'protocol': 'protocol',
        'protocolid': 'protocolid',
        'callerid': 'callerid',
        'deviceid': 'deviceid',
        'provisioningid': 'provisioningid',
        'num': 'num'
    }

    _RELATION = {}

    def __init__(self, *args, **kwargs):
        AbstractModels.__init__(self, *args, **kwargs)

    @property
    def interface(self):
        return '%s/%s' % (self.protocol.upper(), self.name)


class LineSIP(Line):

    MANDATORY = Line.MANDATORY + [
        'username',
        'secret'
    ]

    # mapping = {db_field: model_field}
    _MAPPING = dict(Line._MAPPING.items() + {
        'username': 'username',
        'secret': 'secret'
    }.items())

    def __init__(self, *args, **kwargs):
        self.protocol = 'sip'
        Line.__init__(self, *args, **kwargs)


class LineIAX(Line):

    MANDATORY = Line.MANDATORY + [
        'username',
        'secret'
    ]

    # mapping = {db_field: model_field}
    _MAPPING = dict(Line._MAPPING.items() + {
        'username': 'username',
        'secret': 'secret'
    }.items())

    def __init__(self, *args, **kwargs):
        self.protocol = 'iax'
        Line.__init__(self, *args, **kwargs)


class LineSCCP(Line):

    MANDATORY = Line.MANDATORY + []

    # mapping = {db_field: model_field}
    _MAPPING = dict(Line._MAPPING.items() + {}.items())

    def __init__(self, *args, **kwargs):
        self.protocol = 'sccp'
        Line.__init__(self, *args, **kwargs)


class LineCUSTOM(Line):

    MANDATORY = Line.MANDATORY + []

    # mapping = {db_field: model_field}
    _MAPPING = dict(Line._MAPPING.items() + {}.items())

    def __init__(self, *args, **kwargs):
        self.protocol = 'custom'
        Line.__init__(self, *args, **kwargs)
