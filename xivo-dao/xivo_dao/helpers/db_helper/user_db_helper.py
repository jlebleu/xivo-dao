# -*- coding: UTF-8 -*-

from sqlalchemy.sql.expression import and_

from xivo_dao.alchemy.callfiltermember import Callfiltermember
from xivo_dao.alchemy.dialaction import Dialaction
from xivo_dao.alchemy.extension import Extension as ExtensionSchema
from xivo_dao.alchemy.linefeatures import LineFeatures as LineSchema
from xivo_dao.alchemy.phonefunckey import PhoneFunckey
from xivo_dao.alchemy.queuemember import QueueMember
from xivo_dao.alchemy.rightcallmember import RightCallMember
from xivo_dao.alchemy.schedulepath import SchedulePath
from xivo_dao.alchemy.user_line import UserLine as UserLineSchema
from xivo_dao.alchemy.userfeatures import UserFeatures as UserSchema
from xivo_dao.helpers.db_manager import daosession
from xivo_dao.helpers import db_helper_utils


@daosession
def get_user(session, user_id):
    row = (session.query(UserSchema)
                  .filter(UserSchema.id == user_id)
                  .first())
    if not row:
        return None

    return row


@daosession
def get_user_by_exten_context(session, exten, context):
    row = (session.query(UserSchema)
                  .join(ExtensionSchema, and_(ExtensionSchema.context == context,
                                            ExtensionSchema.exten == exten,
                                            ExtensionSchema.commented == 0))
                  .join(LineSchema, and_(LineSchema.commented == 0))
                  .join(UserLineSchema, and_(UserLineSchema.user_id == UserSchema.id,
                                            UserLineSchema.extension_id == ExtensionSchema.id,
                                           UserLineSchema.line_id == LineSchema.id,
                                           UserLineSchema.main_line == True))
                .first())

    if not row:
        return None

    return row


@daosession
def find_all_user(session):
    rows = session.query(UserSchema).all()

    if not rows:
        return []

    return rows


@daosession
def find_all_user_by_firstname_lastname(session, firstname, lastname):
    rows = (session.query(UserSchema)
                   .filter(UserSchema.firstname == firstname)
                   .filter(UserSchema.lastname == lastname)
                   .all())
    if not rows:
        return []

    return rows


def add_user(**kwargs):
    kwargs.setdefault('id', db_helper_utils.give_me_an_id())
    kwargs.setdefault('firstname', 'XiVO')
    kwargs.setdefault('lastname', 'Avencall')
    kwargs.setdefault('callerid', u'"%s %s"' % (kwargs['firstname'], kwargs['lastname']))

    return db_helper_utils.add_me(UserSchema, **kwargs)


@daosession
def delete_user(session, user_id):
    session.begin()

    (session.query(UserSchema).filter(UserSchema.id == user_id).delete())
    (session.query(QueueMember).filter(QueueMember.usertype == 'user')
                               .filter(QueueMember.userid == user_id)
                               .delete())
    (session.query(RightCallMember).filter(RightCallMember.type == 'user')
                                   .filter(RightCallMember.typeval == str(user_id))
                                   .delete())
    (session.query(Callfiltermember).filter(Callfiltermember.type == 'user')
                                    .filter(Callfiltermember.typeval == str(user_id))
                                    .delete())
    (session.query(Dialaction).filter(Dialaction.category == 'user')
                              .filter(Dialaction.categoryval == str(user_id))
                              .delete())
    (session.query(PhoneFunckey).filter(PhoneFunckey.iduserfeatures == user_id).delete())
    (session.query(SchedulePath).filter(SchedulePath.path == 'user')
                                .filter(SchedulePath.pathid == user_id)
                                .delete())

    session.commit()


def link_user_and_voicemail(user_id, voicemail_id):
    user_row = get_user(user_id)
    if user_row:
        user_row.voicemailenable = 1
        user_row.voicemailtype = 'asterisk'
        user_row.voicemailid = voicemail_id

        if not user_row.language:
            user_row.language = 'fr_FR'

        return db_helper_utils.exec_me(user_row)


def unlink_user_and_voicemail(user_id):
    user_row = get_user(user_id)
    if user_row:
        user_row.voicemailenable = 0
        user_row.voicemailtype = None
        user_row.voicemailid = None

        return db_helper_utils.exec_me(user_row)
