# -*- coding: UTF-8 -*-

import random

from xivo_dao.alchemy.usersip import UserSIP
from xivo_dao.alchemy.staticsip import StaticSIP
from xivo_dao.alchemy.sipauthentication import SIPAuthentication
from xivo_dao.helpers import db_helper_utils


def add_proto_sip(**kwargs):
    kwargs.setdefault('id', db_helper_utils.give_me_an_id())
    kwargs.setdefault('name', ''.join(random.choice('0123456789ABCDEF') for _ in range(6)))
    kwargs.setdefault('context', 'default')
    kwargs.setdefault('type', 'friend')
    kwargs.setdefault('category', 'user')
    kwargs.setdefault('call_limit', 10)

    return db_helper_utils.add_me(UserSIP, **kwargs)


def add_sip_general_settings(**kwargs):
    kwargs.setdefault('id', db_helper_utils.give_me_an_id())
    kwargs.setdefault('cat_metric', 0)
    kwargs.setdefault('var_metric', 0)
    kwargs.setdefault('commented', 0)
    kwargs.setdefault('filename', 'sip.conf')
    kwargs.setdefault('category', 'general')
    kwargs.setdefault('var_name', ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(6)))
    kwargs.setdefault('var_val', ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(6)))

    return db_helper_utils.add_me(StaticSIP, **kwargs)


def add_sip_authentication(**kwargs):
    kwargs.setdefault('id', db_helper_utils.give_me_an_id())
    kwargs.setdefault('usersip_id', db_helper_utils.give_me_an_id())
    kwargs.setdefault('user', ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(6)))
    kwargs.setdefault('secretmode', 'md5')
    kwargs.setdefault('secret', ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(6)))
    kwargs.setdefault('realm', ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(6)))

    return db_helper_utils.add_me(SIPAuthentication, **kwargs)
