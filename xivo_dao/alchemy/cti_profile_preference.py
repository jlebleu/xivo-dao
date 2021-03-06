# -*- coding: utf-8 -*-

# Copyright (C) 2012-2014 Avencall
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

from sqlalchemy.schema import Column, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import relationship

from xivo_dao.helpers.db_manager import Base


class CtiProfilePreference(Base):

    __tablename__ = 'cti_profile_preference'
    __table_args__ = (
        PrimaryKeyConstraint('profile_id', 'preference_id'),
        ForeignKeyConstraint(('profile_id',),
                             ('cti_profile.id',),
                             ondelete='CASCADE'),
        ForeignKeyConstraint(('preference_id',),
                             ('cti_preference.id',),
                             ondelete='CASCADE'),
    )

    profile_id = Column(Integer)
    preference_id = Column(Integer)
    value = Column(String(255))

    cti_profile = relationship("CtiProfile")
    cti_preference = relationship("CtiPreference")
