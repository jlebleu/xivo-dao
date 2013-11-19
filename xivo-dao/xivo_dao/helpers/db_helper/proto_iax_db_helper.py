# -*- coding: UTF-8 -*-

import random

from xivo_dao.alchemy.useriax import UserIAX
from xivo_dao.alchemy.staticiax import StaticIAX
from xivo_dao.helpers import db_helper_utils


def add_iax_general_settings(**kwargs):
    kwargs.setdefault('id', db_helper_utils.give_me_an_id())
    kwargs.setdefault('cat_metric', 0)
    kwargs.setdefault('var_metric', 0)
    kwargs.setdefault('commented', 0)
    kwargs.setdefault('filename', 'sip.conf')
    kwargs.setdefault('category', 'general')
    kwargs.setdefault('var_name', ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(6)))
    kwargs.setdefault('var_val', ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(6)))

    return db_helper_utils.add_me(StaticIAX, **kwargs)


def add_proto_iax(**kwargs):
    kwargs.setdefault('id', db_helper_utils.give_me_an_id())
    kwargs.setdefault('name', ''.join(random.choice('0123456789ABCDEF') for _ in range(6)))
    kwargs.setdefault('context', 'default')
    kwargs.setdefault('type', 'friend')

    return db_helper_utils.add_me(UserIAX, **kwargs)
