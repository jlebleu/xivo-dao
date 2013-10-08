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

import string
import random

from sqlalchemy.sql import and_
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from xivo_dao.alchemy.linefeatures import LineFeatures as LineSchema
from xivo_dao.alchemy.usersip import UserSIP as UserSIPSchema
from xivo_dao.alchemy.user_line import UserLine as UserLineSchema
from xivo_dao.alchemy.extension import Extension
from xivo_dao.helpers.db_manager import daosession
from xivo_dao.data_handler.exception import ElementNotExistsError, \
    ElementDeletionError, ElementCreationError, ElementEditionError
from model import db_converter
from xivo_dao.data_handler.line.model import LineOrdering


DEFAULT_ORDER = [LineOrdering.name, LineOrdering.context]


@daosession
def get(session, line_id):
    line_row = _get_line_row(session, line_id)
    return _row_to_line_model(session, line_row)


def get_by_user_id(user_id):
    line = find_by_user_id(user_id)
    if not line:
        raise ElementNotExistsError('Line', user_id=user_id)

    return line


@daosession
def get_by_number_context(session, number, context):
    line_row = (
        _new_query(session)
        .join(Extension, and_(Extension.exten == number,
                              Extension.context == context))
        .join(UserLineSchema, and_(UserLineSchema.extension_id == Extension.id,
                                   LineSchema.id == UserLineSchema.line_id,
                                   UserLineSchema.main_line == True,
                                   UserLineSchema.main_user == True))
    ).first()

    if not line_row:
        raise ElementNotExistsError('Line', number=number, context=context)

    return _row_to_line_model(session, line_row)


@daosession
def find_all(session, order=None):
    line_rows = _new_query(session, order).all()

    return _rows_to_line_model(session, line_rows)


@daosession
def find_all_by_protocol(session, protocol, order=None):
    line_rows = (_new_query(session, order)
                 .filter(LineSchema.protocol == protocol.lower())
                 .all())

    return _rows_to_line_model(session, line_rows)


@daosession
def find_all_by_name(session, name, order=None):
    search = '%%%s%%' % name.lower()

    line_rows = (_new_query(session, order)
                 .filter(LineSchema.name.ilike(search))
                 .all())

    return _rows_to_line_model(session, line_rows)


@daosession
def find_all_by_device_id(session, device_id, order=None):
    line_rows = (_new_query(session, order)
                 .filter(LineSchema.device == str(device_id))
                 .all())

    return _rows_to_line_model(session, line_rows)


@daosession
def find_by_user_id(session, user_id, main_line=True, main_user=True):
    line_row = (_new_query(session)
                .join(UserLineSchema,
                      and_(UserLineSchema.user_id == user_id,
                           UserLineSchema.line_id == LineSchema.id,
                           UserLineSchema.main_line == main_line,
                           UserLineSchema.main_user == main_user))
                .first())

    if line_row:
        return _row_to_line_model(session, line_row)
    return None


def _rows_to_line_model(session, line_rows):
    if not line_rows:
        return []

    lines = []
    for line_row in line_rows:
        lines.append(_row_to_line_model(session, line_row))

    return lines


def _row_to_line_model(session, line_row):
    protocol_row = _get_protocol_row(session, line_row)
    return db_converter.to_model(line_row, protocol_row)


def _get_protocol_row(session, line):
    protocol = line.protocol.lower()
    if protocol == 'sip':
        row = session.query(UserSIPSchema).filter(line.protocolid == UserSIPSchema.id).first()
    else:
        raise NotImplementedError("Only SIP lines are supported")

    if not row:
        raise ElementNotExistsError('Line %s' % protocol, id=line.protocolid)

    return row


@daosession
def reset_device(session, device_id):
    session.query(LineSchema).filter(LineSchema.device == str(device_id)).update({'device': ''})


@daosession
def provisioning_id_exists(session, provd_id):
    count = session.query(LineSchema.id).filter(LineSchema.provisioningid == provd_id).count()
    return count > 0


@daosession
def create(session, line):
    line_row, protocol_row = db_converter.to_source(line)

    _create_row(session, protocol_row)
    line_row.protocolid = protocol_row.id
    _create_row(session, line_row)

    return _row_to_line_model(session, line_row)


def _create_row(session, row):
    session.begin()
    session.add(row)

    try:
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise ElementCreationError('Line', e)


@daosession
def edit(session, line):
    line_row, protocol_row = _get_line_and_protocol(session, line)
    db_converter.update_source(line_row, protocol_row, line)

    session.begin()
    session.add(line_row)
    session.add(protocol_row)

    try:
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise ElementEditionError('Line', e)


def _get_line_and_protocol(session, line):
    line_row = _get_line_row(session, line.id)
    protocol_row = _get_protocol_row(session, line)
    return line_row, protocol_row


def _get_line_row(session, line_id):
    line_row = _new_query(session).filter(LineSchema.id == line_id).first()

    if not line_row:
        raise ElementNotExistsError('Line', line_id=line_id)

    return line_row


@daosession
def update_xivo_userid(session, line, main_user):
    if line.protocol.lower() == 'sip':
        session.begin()
        protocol_row = _get_protocol_row(session, line)
        protocol_row.setvar = 'XIVO_USERID=%s' % main_user.id
        session.add(protocol_row)

        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise ElementEditionError('Line', e)


@daosession
def generate_username(session):
    return generate_random_hash(session, UserSIPSchema.username)


@daosession
def generate_secret(session):
    return generate_random_hash(session, UserSIPSchema.secret)


def generate_random_hash(session, column):
    token = random_hash()
    query = session.query(column)

    count = query.filter(column == token).count()
    while count > 0:
        token = random_hash()
        count = query.filter(column == token).count()

    return token


def random_hash(length=8):
    pool = string.lowercase + string.digits
    return ''.join(random.choice(pool) for _ in range(length))


@daosession
def delete(session, line):
    line_row, protocol_row = _get_line_and_protocol(session, line)
    _delete_rows(session, line_row, protocol_row)


def _delete_rows(session, line_row, protocol_row):
    session.begin()
    session.delete(line_row)
    session.delete(protocol_row)

    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise ElementDeletionError('Line', 'line still has a link')
    except SQLAlchemyError, e:
        session.rollback()
        raise ElementDeletionError('Line', e)


def _new_query(session, order=None):
    order = order or DEFAULT_ORDER
    return session.query(LineSchema).filter(LineSchema.commented == 0).order_by(*order)


@daosession
def associate_extension(session, extension, line_id):
    line_row = (session.query(LineSchema)
                .filter(LineSchema.id == line_id)
                .first())

    if line_row:
        line_row.number = extension.exten
        line_row.context = extension.context

        session.begin()
        session.add(line_row)
        session.commit()


@daosession
def unassociate_extension(session, extension):
    line_row = (session.query(LineSchema)
                .filter(LineSchema.number == extension.exten)
                .filter(LineSchema.context == extension.context)
                .first())

    if line_row:
        line_row.number = ''
        line_row.context = ''
        line_row.provisioningid = 0

        session.begin()
        session.add(line_row)
        session.commit()
