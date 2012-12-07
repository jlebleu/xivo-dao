# -*- coding: utf-8 -*-

# Copyright (C) 2012  Avencall

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA..


from mock import Mock, patch
from xivo_dao.alchemy.queuemember import QueueMember
from xivo_dao import queue_member_dao
from xivo_dao.helpers.queuemember_formatter import QueueMemberFormatter
from xivo_dao.tests.test_dao import DAOTestCase


class TestQueueMemberDAO(DAOTestCase):

    tables = []

    def test_get_queuemembers(self):
        with patch.object(self.session, 'query') as mock_query:
            old_queuemember_formatter = QueueMemberFormatter.format_queuemembers
            QueueMemberFormatter.format_queuemembers = Mock()

            queue_member_dao.get_queuemembers()

            try:
                mock_query.assert_called_with(QueueMember)
                self.assertTrue(QueueMemberFormatter.format_queuemembers.called)
            finally:
                QueueMemberFormatter.format_queuemembers = old_queuemember_formatter