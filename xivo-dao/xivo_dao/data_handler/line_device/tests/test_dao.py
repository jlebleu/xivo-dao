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

from hamcrest import assert_that, is_, same_instance
from mock import Mock, patch

from xivo_dao.alchemy.linefeatures import LineFeatures as LineSchema
from xivo_dao.data_handler.device.model import Device
from xivo_dao.data_handler.line.model import LineSIP
from xivo_dao.data_handler.exception import ElementNotExistsError
from xivo_dao.tests.test_dao import DAOTestCase

from .. import dao


class TestLineDeviceDao(DAOTestCase):

    tables = [LineSchema]

    @patch('xivo_dao.data_handler.device.dao.find')
    def test_find_device_from_line_no_line(self, device_find):
        line = Mock(id=498)

        self.assertRaises(ElementNotExistsError, dao.find_device_from_line, line)

    @patch('xivo_dao.data_handler.device.dao.find')
    def test_find_device_from_line_no_device(self, device_find):
        device_id = 'ad0a12fd5f244ae68a3c626789203698'
        line_row = self.add_line(device=device_id)
        line = LineSIP.from_data_source(line_row)
        device_find.side_effect = ElementNotExistsError('Device', id=device_id)

        self.assertRaises(ElementNotExistsError, dao.find_device_from_line, line)

    @patch('xivo_dao.data_handler.device.dao.find')
    def test_find_device_from_line(self, device_find):
        device_id = 'ad0a12fd5f244ae68a3c626789203698'
        line_row = self.add_line(device=device_id)
        line = LineSIP.from_data_source(line_row)
        device = device_find.return_value = Mock(Device)

        result = dao.find_device_from_line(line)

        device_find.assert_called_once_with(device_id)
        assert_that(result, is_(same_instance(device)))
