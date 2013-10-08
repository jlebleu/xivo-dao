# -*- coding: utf-8 -*-

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

from xivo_dao.alchemy.extension import Extension as ExtensionSchema
from xivo_dao.converters.database_converter import DatabaseConverter
from xivo_dao.helpers.abstract_model import AbstractModels


DB_TO_MODEL_MAPPING = {
    'id': 'id',
    'exten': 'exten',
    'context': 'context',
    'type': 'type',
    'typeval': 'typeval',
    'commented': 'commented'
}


class Extension(AbstractModels):

    MANDATORY = [
        'exten',
        'context',
        'type',
        'typeval'
    ]

    FIELDS = [
        'id',
        'exten',
        'context',
        'type',
        'typeval',
        'commented',
    ]

    _RELATION = {}

    def __init__(self, *args, **kwargs):
        AbstractModels.__init__(self, *args, **kwargs)
        if self.commented is None:
            self.commented = False


class ExtensionDBConverter(DatabaseConverter):
    def __init__(self):
        DatabaseConverter.__init__(self, DB_TO_MODEL_MAPPING, ExtensionSchema, Extension)

    def to_model(self, db_row):
        model = DatabaseConverter.to_model(self, db_row)
        if hasattr(model, 'commented') and isinstance(model.commented, int):
            model.commented = bool(model.commented)
        return model

    def to_source(self, model):
        if hasattr(model, 'commented') and isinstance(model.commented, bool):
            model.commented = int(model.commented)
        return DatabaseConverter.to_source(self, model)


class ExtensionOrdering(object):
    exten = ExtensionSchema.exten
    context = ExtensionSchema.context


db_converter = ExtensionDBConverter()
