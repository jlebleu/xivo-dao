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

from sqlalchemy.schema import Column
from sqlalchemy.types import DateTime, Integer, String, Boolean, Interval

from xivo_dao.helpers.db_manager import Base


class CallLog(Base):

    __tablename__ = 'call_log'

    id = Column(Integer, nullable=False, primary_key=True)
    date = Column(DateTime, nullable=False)
    source_name = Column(String(255))
    source_exten = Column(String(255))
    source_line_identity = Column(String(255))
    destination_name = Column(String(255))
    destination_exten = Column(String(255))
    destination_line_identity = Column(String(255))
    duration = Column(Interval, nullable=False)
    user_field = Column(String(255))
    answered = Column(Boolean)
