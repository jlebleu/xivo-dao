# -*- coding: UTF-8 -*-

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

import unittest

from mock import patch, Mock
from .. import services


class TestDeviceServices(unittest.TestCase):

    @patch('xivo_dao.data_handler.line_device.dao.find_device_from_line')
    def test_find_from_line(self, dao_find_from_line):
        device = dao_find_from_line.return_value = Mock()
        line = Mock()

        result = services.find_device_from_line(line)

        self.assertEquals(result, device)
        dao_find_from_line.assert_called_once_with(line)
