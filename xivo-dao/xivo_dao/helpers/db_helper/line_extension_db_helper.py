# -*- coding: UTF-8 -*-

from xivo_dao.alchemy.user_line import UserLine as UserLineSchema
from xivo_dao.helpers.db_helper import extension_db_helper
from xivo_dao.helpers.db_manager import daosession


@daosession
def find_all_line_extension(session, line_extension_id):
    rows = (session.query(UserLineSchema)
                   .filter(UserLineSchema.id == line_extension_id)
                   .all())
    if not rows:
        return []

    return rows


@daosession
def find_all_line_extension_by_extension_id(session, extension_id):
    rows = (session.query(UserLineSchema)
                   .filter(UserLineSchema.extension_id == extension_id)
                   .all())
    if not rows:
        return []

    return rows


@daosession
def find_all_line_extension_by_user_id(session, user_id):
    row = (session.query(UserLineSchema)
                  .filter(UserLineSchema.user_id == user_id)
                  .all())
    if not row:
        return []

    return row


@daosession
def find_all_line_extension_by_line_id(session, line_id):
    rows = (session.query(UserLineSchema)
                   .filter(UserLineSchema.line_id == line_id)
                   .all())
    if not rows:
        return []

    return rows


@daosession
def add_line_extension(session, **kwargs):
    (session.query(UserLineSchema)
            .filter(UserLineSchema.line_id == int(kwargs['line_id']))
            .filter(UserLineSchema.extension_id == None)
            .update({'extension_id': int(kwargs['extension_id'])}))


@daosession
def delete_line_extension(session, line_extension_id):
    for ule in find_all_line_extension(line_extension_id):
        unlink_line_extension_by_line_extension_id(ule.id)


def unlink_line_extension_by_number_context(exten, context):
    extension = extension_db_helper.find_extension_by_exten_context(exten, context)

    if extension:
        for ule in find_all_line_extension_by_extension_id(extension.id):
            unlink_line_extension_by_line_extension_id(ule.id)


def unlink_line_extension_by_line_id(line_id):
    for ule in find_all_line_extension_by_line_id(line_id):
        unlink_line_extension_by_line_extension_id(ule.id)


def unlink_line_extension_by_user_id(user_id):
    for ule in find_all_line_extension_by_user_id(user_id):
        unlink_line_extension_by_line_extension_id(ule.id)


def unlink_line_extension_by_extension_id(extension_id):
    for ule in find_all_line_extension_by_extension_id(extension_id):
        unlink_line_extension_by_line_extension_id(ule.id)


@daosession
def unlink_line_extension_by_line_extension_id(session, line_extension_id):
    data_dict = {'extension_id': None}
    session.query(UserLineSchema).filter(UserLineSchema.id == line_extension_id).update(data_dict)
