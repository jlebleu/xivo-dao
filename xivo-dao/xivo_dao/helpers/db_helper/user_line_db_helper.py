# -*- coding: UTF-8 -*-

from xivo_dao.alchemy.user_line import UserLine as UserLineSchema
from xivo_dao.helpers.db_manager import daosession
from xivo_dao.helpers import db_helper_utils
from xivo_dao.helpers.db_helper import extension_db_helper


@daosession
def find_all_by_extension_id(session, extension_id):
    row = (session.query(UserLineSchema)
                  .filter(UserLineSchema.extension_id == extension_id)
                  .all())
    if not row:
        return []

    return row


@daosession
def find_all_by_user_id(session, user_id):
    row = (session.query(UserLineSchema)
                  .filter(UserLineSchema.user_id == user_id)
                  .all())
    if not row:
        return []

    return row


@daosession
def find_all_by_line_id(session, line_id):
    row = (session.query(UserLineSchema)
                  .filter(UserLineSchema.line_id == line_id)
                  .all())
    if not row:
        return []

    return row


def add_user_line(**kwargs):
    kwargs.setdefault('id', db_helper_utils.give_me_an_id())
    kwargs.setdefault('main_user', True)
    kwargs.setdefault('main_line', True)

    return db_helper_utils.add_me(UserLineSchema, **kwargs)


def delete_user_line_by_number_context(exten, context):
    extension = extension_db_helper.find_extension_by_exten_context(exten, context)

    if extension:
        for user_line in find_all_by_extension_id(extension.id):
            delete_user_line(user_line.id)


def delete_user_line_by_user_id(user_id):
    for user_line in find_all_by_user_id(user_id):
        delete_user_line(user_line.id)


def delete_user_line_by_line_id(line_id):
    for user_line in find_all_by_line_id(line_id):
        delete_user_line(user_line.id)


@daosession
def delete_user_line(session, user_line_id):
    session.begin()
    session.query(UserLineSchema).filter(UserLineSchema.id == user_line_id).delete()
    session.commit()
