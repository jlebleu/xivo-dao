# -*- coding: utf-8 -*-

# Copyright (C) 2007-2014 Avencall
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

from xivo_dao import extensions_dao
from xivo_dao.alchemy.extension import Extension
from xivo_dao.tests.test_dao import DAOTestCase


class TestExtensionsDAO(DAOTestCase):

    def test_exten_by_name(self):
        self.add_extension(type='extenfeatures',
                           typeval='enablednd',
                           exten='*25')
        self.add_extension(type='extenfeatures',
                           typeval='phoneprogfunckey',
                           exten='_*735')
        enablednd = extensions_dao.exten_by_name('enablednd')
        phoneprogfunckey = extensions_dao.exten_by_name('phoneprogfunckey')

        self.assertEqual(enablednd, '*25')
        self.assertEqual(phoneprogfunckey, '_*735')

    def test_create(self):
        exten = Extension()
        exten.type = 'user'
        exten.exten = '2000'
        exten.context = 'default'

        extensions_dao.create(exten)
        self.assertTrue(exten.id)
        self.assertTrue(exten in self._get_all())
        self.assertEquals(exten.name, exten.typeval)

    def test_get_by_exten(self):
        self.add_extension(type='extenfeatures',
                           typeval='enablednd',
                           exten='*25')
        result = extensions_dao.get_by_exten('*25')
        self.assertEquals('*25', result.exten)

    def _get_all(self):
        return self.session.query(Extension).all()

    def test_delete_by_exten(self):
        self.add_extension(type='extenfeatures',
                           typeval='enablednd',
                           exten='*25')
        self.add_extension(type='extenfeatures',
                           typeval='phoneprogfunckey',
                           exten='_*735')
        extensions_dao.delete_by_exten("*25")
        self.assertFalse("*25" in [item.exten for item in self._get_all()])
        self.assertTrue("_*735" in [item.exten for item in self._get_all()])
