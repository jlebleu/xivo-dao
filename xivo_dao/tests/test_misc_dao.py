# -*- coding: utf-8 -*-

# Copyright (C) 2014 Avencall
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

import time

from hamcrest import assert_that
from hamcrest import less_than

from xivo_dao import misc_dao
from xivo_dao.tests.test_dao import DAOTestCase


class TestMiscDAO(DAOTestCase):

    def test_pg_sleep(self):
        seconds = 2

        start = time.time()

        misc_dao.pg_sleep(seconds)

        end = time.time()

        delta = end - start

        assert_that(abs(delta - seconds), less_than(0.1))
