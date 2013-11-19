# -*- coding: UTF-8 -*-


from xivo_dao.alchemy.sccpline import SCCPLine as SCCPLineSchema
from xivo_dao.alchemy.sccpdevice import SCCPDevice as SCCPDeviceSchema
from xivo_dao.alchemy.sccpgeneralsettings import SCCPGeneralSettings
from xivo_dao.helpers import db_helper_utils


def add_sccpdevice(**kwargs):
    kwargs.setdefault('id', db_helper_utils.give_me_an_id())
    kwargs.setdefault('name', 'SEP001122334455')
    kwargs.setdefault('device', 'SEP001122334455')
    kwargs.setdefault('line', '1000')
    kwargs.setdefault('voicemail', '1234')

    return db_helper_utils.add_me(SCCPDeviceSchema, **kwargs)


def add_proto_sccp(**kwargs):
    kwargs.setdefault('id', db_helper_utils.give_me_an_id())
    kwargs.setdefault('name', '1234')
    kwargs.setdefault('context', 'default')
    kwargs.setdefault('cid_name', 'Tester One')
    kwargs.setdefault('cid_num', '1234')

    return db_helper_utils.add_me(SCCPLineSchema, **kwargs)


def add_sccp_general_settings(**kwargs):
    kwargs.setdefault('id', db_helper_utils.give_me_an_id())
    kwargs.setdefault('option_name', 'directmedia')
    kwargs.setdefault('option_value', 'no')

    return db_helper_utils.add_me(SCCPGeneralSettings, **kwargs)
