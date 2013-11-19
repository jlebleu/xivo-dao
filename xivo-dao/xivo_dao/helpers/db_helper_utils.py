# -*- coding: UTF-8 -*-

import random
from xivo_dao.helpers.db_manager import daosession


@daosession
def add_me(session, db_obj, **kwargs):
    data_dict = {}
    for arg in kwargs:
        if hasattr(db_obj, arg):
            data_dict[arg] = kwargs[arg]

    res = db_obj(**data_dict)

    session.begin()
    try:
        session.add(res)
        session.commit()
    except Exception:
        session.rollback()
        raise

    return res


@daosession
def exec_me(session, db_obj):
    session.begin()
    try:
        session.add(db_obj)
        session.commit()
    except Exception:
        session.rollback()
        raise

    return db_obj


def give_me_an_id():
    return random.randint(1, 1000000)
