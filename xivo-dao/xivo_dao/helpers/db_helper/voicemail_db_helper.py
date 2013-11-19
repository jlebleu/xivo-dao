# -*- coding: UTF-8 -*-

import random

from xivo_dao.alchemy.voicemail import Voicemail as VoicemailSchema
from xivo_dao.alchemy.staticvoicemail import StaticVoicemail
from xivo_dao.helpers import db_helper_utils
from xivo_dao.helpers.db_manager import daosession


@daosession
def find_voicemail_by_number_context(session, number, context):
    row = (session.query(VoicemailSchema)
                  .filter(VoicemailSchema.mailbox == number)
                  .filter(VoicemailSchema.context == context)
                  .first())
    if not row:
        return None

    return row


def add_voicemail(**kwargs):
    kwargs.setdefault('uniqueid', db_helper_utils.give_me_an_id())
    kwargs.setdefault('fullname', 'Auto Voicemail')
    kwargs.setdefault('mailbox', ''.join(random.choice('0123456789_*X.') for _ in range(6)))
    kwargs.setdefault('context', 'default')
    kwargs.setdefault('language', 'en_US')

    return db_helper_utils.add_me(VoicemailSchema, **kwargs)


def add_voicemail_general_settings(**kwargs):
    kwargs.setdefault('id', db_helper_utils.give_me_an_id())
    kwargs.setdefault('cat_metric', 0)
    kwargs.setdefault('var_metric', 0)
    kwargs.setdefault('commented', 0)
    kwargs.setdefault('filename', 'voicemail.conf')
    kwargs.setdefault('category', 'general')
    kwargs.setdefault('var_name', ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(6)))
    kwargs.setdefault('var_val', ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(6)))

    return db_helper_utils.add_me(StaticVoicemail, **kwargs)


@daosession
def delete_voicemail(session, voicemail_id):
    session.begin()

    (session.query(VoicemailSchema).filter(VoicemailSchema.uniqueid == voicemail_id).delete())

    session.commit()


@daosession
def delete_voicemail_by_number_context(session, number, context):
    session.begin()

    (session.query(VoicemailSchema)
            .filter(VoicemailSchema.mailbox == number)
            .filter(VoicemailSchema.context == context)
            .delete())

    session.commit()
