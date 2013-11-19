# -*- coding: UTF-8 -*-

import random

from sqlalchemy.sql.expression import and_

from xivo_dao.alchemy.user_line import UserLine as UserLineSchema
from xivo_dao.alchemy.linefeatures import LineFeatures as LineSchema
from xivo_dao.alchemy.extension import Extension as ExtensionSchema
from xivo_dao.helpers import db_helper_utils
from xivo_dao.helpers.db_manager import daosession


@daosession
def get_line(session, line_id):
    row = (session.query(LineSchema)
                  .filter(LineSchema.id == line_id)
                  .first())
    if not row:
        return None

    return row


@daosession
def find_line_by_exten_context(session, exten, context):
    row = (session.query(LineSchema)
                  .join(ExtensionSchema, and_(ExtensionSchema.exten == exten,
                                              ExtensionSchema.context == context))
                  .join(UserLineSchema, and_(UserLineSchema.extension_id == ExtensionSchema.id,
                                             LineSchema.id == UserLineSchema.line_id))
           ).first()

    if not row:
        return None

    return row


def add_line(**kwargs):
    kwargs.setdefault('id', db_helper_utils.give_me_an_id())
    kwargs.setdefault('name', ''.join(random.choice('0123456789ABCDEF') for _ in range(6)))
    kwargs.setdefault('protocol', 'sip')
    kwargs.setdefault('protocolid', db_helper_utils.give_me_an_id())
    kwargs.setdefault('provisioningid', int(''.join(random.choice('123456789') for _ in range(6))))
    kwargs.setdefault('exten', '%s' % random.randint(1000, 1999))
    kwargs.setdefault('context', 'default')
    kwargs.setdefault('device', '')
    kwargs.setdefault('commented', 0)

    return db_helper_utils.add_me(LineSchema, **kwargs)


@daosession
def delete_line(session, line_id):
    session.begin()
    (session.query(LineSchema)
            .filter(LineSchema.id == line_id)
            .delete())
    session.commit()


@daosession
def delete_line_with_exten_context(session, exten, context):
    session.begin()
    (session.query(LineSchema)
            .filter(LineSchema.number == exten)
            .filter(LineSchema.context == context)
            .delete())
    session.commit()


@daosession
def delete_all(session):
    lines = session.query(LineSchema).all()

    for line in lines:
        links = ule_services.find_all_by_line_id(line.id)
        for link in links:
            try:
                ule_services.delete_everything(link)
            except ElementDeletionError:
                pass
        try:
            line_services.delete(line)
        except ElementDeletionError:
            pass
