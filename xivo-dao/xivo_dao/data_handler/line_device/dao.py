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

from xivo_dao.alchemy.linefeatures import LineFeatures as LineSchema
from xivo_dao.data_handler.device import dao as device_dao
from xivo_dao.data_handler.exception import ElementNotExistsError
from xivo_dao.helpers.db_manager import daosession

import logging
logger = logging.getLogger(__name__)


@daosession
def find_device_from_line(session, line):
    device_row = session.query(LineSchema).filter(LineSchema.id == line.id).first()
    if not device_row:
        raise ElementNotExistsError('Line', id=line.id)
    return device_dao.find(device_row.device)
