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
from xivo_dao.alchemy.linefeatures import LineFeatures as LineSchema
from xivo_dao.alchemy.usersip import UserSIP as UserSIPSchema
from xivo_dao.alchemy.sccpline import SCCPLine as SCCPLineSchema
from xivo_dao.converters.database_converter import DatabaseConverter


class LineSIP(AbstractModels):

    MANDATORY = [
        'context',
        'protocol',
        'device_slot'
    ]

    FIELDS = [
        'id',
        'number',
        'context',
        'protocol',
        'protocolid',
        'callerid',
        'device',
        'provisioning_extension',
        'configregistrar',
        'device_slot',
        'username',
        'secret'
    ]

    _RELATION = {}

    @property
    def interface(self):
        return '%s/%s' % (self.protocol.upper(), self.name)

    def __init__(self, *args, **kwargs):
        AbstractModels.__init__(self, *args, **kwargs)
        self.protocol = 'sip'


class LineSCCP(AbstractModels):

    MANDATORY = [
        'context',
        'protocol',
        'device_slot'
    ]

    FIELDS = [
        'id',
        'number',
        'context',
        'protocol',
        'protocolid',
        'callerid',
        'device',
        'provisioning_extension',
        'configregistrar',
        'device_slot',
    ]

    _RELATION = {}

    @property
    def interface(self):
        return '%s/%s' % (self.protocol.upper(), self.name)

    def __init__(self, *args, **kwargs):
        AbstractModels.__init__(self, *args, **kwargs)
        self.protocol = 'sccp'


class LineOrdering(object):
        name = LineSchema.name
        context = LineSchema.context


class LineSIPDBConverter(object):

    LINE_TO_MODEL = {
        'id': 'id',
        'name': 'username',
        'number': 'number',
        'context': 'context',
        'protocol': 'protocol',
        'protocolid': 'protocolid',
        'device': 'device',
        'configregistrar': 'configregistrar',
        'provisioningid': 'provisioning_extension',
        'num': 'device_slot',
    }

    PROTOCOL_TO_MODEL = {
        'id': 'protocolid',
        'context': 'context',
        'callerid': 'callerid',
        'name': 'username',
        'secret': 'secret'
    }

    def __init__(self):
        self.line_converter = DatabaseConverter(self.LINE_TO_MODEL, LineSchema, LineSIP)
        self.protocol_converter = DatabaseConverter(self.PROTOCOL_TO_MODEL, UserSIPSchema, LineSIP)

    def to_model(self, line_row, protocol_row):
        model = self.line_converter.to_model(line_row)
        self.protocol_converter.update_model(model, protocol_row)
        return model

    def to_source(self, model):
        line_row = self.line_converter.to_source(model)
        line_row.protocol = 'sip'
        protocol_row = self.protocol_converter.to_source(model)
        protocol_row.username = ''
        protocol_row.type = 'friend'
        protocol_row.category = 'user'

        return line_row, protocol_row

    def update_source(self, line_row, protocol_row, model):
        self.line_converter.update_source(line_row, model)
        self.protocol_converter.update_source(protocol_row, model)


    def update_source(self, line_row, protocol_row, model):
        self.line_converter.update_source(line_row, model)
        self.protocol_converter.update_source(protocol_row, model)


db_converter = LineSIPDBConverter()
