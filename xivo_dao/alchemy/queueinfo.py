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

from sqlalchemy.schema import Column, PrimaryKeyConstraint, Index
from sqlalchemy.types import Integer, String

from xivo_dao.helpers.db_manager import Base


class QueueInfo(Base):

    __tablename__ = 'queue_info'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        Index('queue_info_call_time_t_index', 'call_time_t'),
        Index('queue_info_queue_name_index', 'queue_name'),
    )

    id = Column(Integer)
    call_time_t = Column(Integer)
    queue_name = Column(String(128), nullable=False, server_default='')
    caller = Column(String(80), nullable=False, server_default='')
    caller_uniqueid = Column(String(32), nullable=False, server_default='')
    call_picker = Column(String(80))
    hold_time = Column(Integer)
    talk_time = Column(Integer)
