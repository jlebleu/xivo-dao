# -*- coding: UTF-8 -*-

from xivo_dao.alchemy.extension import Extension as ExtensionSchema
from xivo_dao.helpers import db_helper_utils
from xivo_dao.helpers.db_manager import daosession


@daosession
def find_all_extension(session):
    rows = session.query(ExtensionSchema).all()

    if not rows:
        return []

    return rows


@daosession
def find_extension_by_exten(session, exten):
    row = (session.query(ExtensionSchema)
                  .filter(ExtensionSchema.exten == exten)
                  .first())
    if not row:
        return None

    return row


@daosession
def find_extension_by_exten_context(session, exten, context):
    row = (session.query(ExtensionSchema)
                  .filter(ExtensionSchema.exten == exten)
                  .filter(ExtensionSchema.context == context)
                  .first())
    if not row:
        return None

    return row


def add_extension(**kwargs):
    kwargs.setdefault('id', db_helper_utils.give_me_an_id())
    kwargs.setdefault('type', 'user')
    kwargs.setdefault('context', 'default')
    kwargs.setdefault('typeval', '1')

    if 'commented' in kwargs:
        kwargs['commented'] = int(kwargs['commented'])

    return db_helper_utils.add_me(ExtensionSchema, **kwargs)


@daosession
def delete_extension(session, extension_id):
    session.begin()
    session.query(ExtensionSchema).filter(ExtensionSchema.id == extension_id).delete()
    session.commit()


@daosession
def delete_extension_by_exten_context(session, exten, context):
    session.begin()
    (session.query(ExtensionSchema)
            .filter(ExtensionSchema.exten == exten)
            .filter(ExtensionSchema.context == context)
            .delete())
    session.commit()


@daosession
def delete_extension_by_user_id(session, user_id):
    session.begin()
    (session.query(ExtensionSchema)
            .filter(ExtensionSchema.typeval == str(user_id))
            .filter(ExtensionSchema.type == 'user')
            .delete())
    session.commit()
