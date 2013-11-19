# -*- coding: UTF-8 -*-

import random
from xivo_dao.alchemy.usercustom import UserCustom as UserCustomSchema
from xivo_dao.helpers import db_helper_utils


def add_proto_custom(**kwargs):
    kwargs.setdefault('id', db_helper_utils.give_me_an_id())
    kwargs.setdefault('interface', ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(6)))

    return db_helper_utils.add_me(UserCustomSchema, **kwargs)
