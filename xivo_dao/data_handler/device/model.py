# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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

from xivo_dao.data_handler import errors
from xivo_dao.helpers.new_model import NewModel


class Device(NewModel):

    MANDATORY = [
    ]

    FIELDS = [
        'id',
        'ip',
        'mac',
        'sn',
        'plugin',
        'vendor',
        'model',
        'version',
        'description',
        'status',
        'options',
        'template_id',
    ]

    _RELATION = {}

    def is_switchboard(self):
        if self.plugin and 'switchboard' in self.plugin:
            return True

        return bool(self.options and self.options.get('switchboard'))


class DeviceOrdering(object):
    DIRECTIONS = ['desc', 'asc']

    id = 'id'
    ip = 'ip'
    mac = 'mac'
    plugin = 'plugin'
    model = 'model'
    vendor = 'vendor'
    version = 'version'

    @classmethod
    def all_columns(cls):
        return [cls.id, cls.ip, cls.mac, cls.plugin, cls.model, cls.vendor, cls.version]

    @classmethod
    def from_column_name(cls, column):
        if column in cls.all_columns():
            return column
        return None

    @classmethod
    def directions(cls):
        return cls.DIRECTIONS

    @classmethod
    def validate_order(cls, order):
        if order not in cls.all_columns():
            raise errors.invalid_ordering(order)

    @classmethod
    def validate_direction(cls, direction):
        if direction not in cls.directions():
            raise errors.invalid_direction(direction)
