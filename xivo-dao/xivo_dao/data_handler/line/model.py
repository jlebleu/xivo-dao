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


class LineOrdering(object):
        name = LineSchema.name
        context = LineSchema.context


class LineSIPDBConverter(object):

    def __init__(self):
        pass

    def to_model(self, line_row, protocol_row):
        model = LineSIP()
        self._map_line_columns(model, line_row)
        self._map_protocol_columns(model, protocol_row)
        return model

    def _map_line_columns(self, model, line_row):
        model.id = line_row.id
        model.number = line_row.number
        model.context = line_row.context
        model.protocol = line_row.protocol
        model.device = line_row.device
        model.provisioning_extension = line_row.provisioningid
        model.configregistrar = line_row.configregistrar
        model.device_slot = line_row.num

    def _map_protocol_columns(self, model, protocol_row):
        model.username = protocol_row.name
        model.secret = protocol_row.secret
        model.protocolid = protocol_row.id
        model.callerid = protocol_row.callerid

    def to_source(self, model):
        line_row = self._build_line_row(model)
        protocol_row = self._build_protocol_row(model)

        return line_row, protocol_row

    def _build_line_row(self, model):
        line_row = LineSchema()
        line_row.id = model.id
        line_row.name = model.username
        line_row.number = model.number
        line_row.context = model.context
        line_row.protocol = 'sip'
        line_row.device = model.device
        line_row.provisioningid = model.provisioning_extension
        line_row.configregistrar = model.configregistrar
        line_row.num = model.device_slot

        return line_row

    def _build_protocol_row(self, model):
        protocol_row = UserSIPSchema()
        protocol_row.id = model.protocolid
        protocol_row.name = model.username
        protocol_row.secret = model.secret
        protocol_row.context = model.context
        protocol_row.callerid = model.callerid
        protocol_row.username = ''
        protocol_row.type = 'friend'
        protocol_row.category = 'user'

        return protocol_row

    MODEL_TO_LINE = {
        'id': 'id',
        'username': 'name',
        'number': 'number',
        'context': 'context',
        'protocol': 'protocol',
        'protocolid': 'protocolid',
        'device': 'device',
        'configregistrar': 'configregistrar',
        'provisioning_extension': 'provisioningid',
        'device_slot': 'num',
    }

    MODEL_TO_PROTOCOL = {
        'protocolid': 'id',
        'context': 'context',
        'callerid': 'callerid',
        'username': 'username',
        'secret': 'secret'
    }

    def update_source(self, line_row, protocol_row, model):
        line_converter = DatabaseConverter(self.MODEL_TO_LINE, LineSIP, LineSchema)
        protocol_converter = DatabaseConverter(self.MODEL_TO_PROTOCOL, LineSIP, UserSIPSchema)

        line_converter.update_source(line_row, model)
        protocol_converter.update_source(protocol_row, model)


db_converter = LineSIPDBConverter()
