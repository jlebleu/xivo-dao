# -*- coding: utf-8 -*-

# Copyright (C) 2012-2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from xivo_dao.helpers.db_manager import Base
from sqlalchemy.schema import Column, PrimaryKeyConstraint, UniqueConstraint, \
    Index
from sqlalchemy.types import Integer, String, Text, Enum
from xivo_dao.alchemy import enum


class UserSIP(Base):

    __tablename__ = 'usersip'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        UniqueConstraint('name'),
        Index('usersip__idx__category', 'category'),
        Index('usersip__idx__mailbox', 'mailbox'),
    )

    id = Column(Integer, nullable=False)
    name = Column(String(40), nullable=False)
    type = Column(Enum('friend', 'peer', 'user',
                       name='useriax_type',
                       metadata=Base.metadata),
                  nullable=False)
    username = Column(String(80))
    secret = Column(String(80), nullable=False, server_default='')
    md5secret = Column(String(32), nullable=False, server_default='')
    context = Column(String(39))
    language = Column(String(20))
    accountcode = Column(String(20))
    amaflags = Column(Enum('default', 'omit', 'billing', 'documentation',
                           name='useriax_amaflags',
                           metadata=Base.metadata),
                      nullable=False, server_default='default')
    allowtransfer = Column(Integer)
    cc_agent_policy = Column(Enum('never', 'generic', 'native',
                              name='usersip_cc_agent_policy',
                              metadata=Base.metadata))
    cc_monitor_policy = Column(Enum('never', 'generic', 'native', 'always',
                              name='usersip_cc_monitor_policy',
                              metadata=Base.metadata))
    fromuser = Column(String(80))
    fromdomain = Column(String(255))
    mailbox = Column(String(80))
    subscribemwi = Column(Integer, nullable=False, server_default='0')
    buggymwi = Column(Integer)
    call_limit = Column('call-limit', Integer, nullable=False, server_default='0')
    callerid = Column(String(160))
    fullname = Column(String(80))
    cid_number = Column(String(80))
    maxcallbitrate = Column(Integer)
    insecure = Column(Enum('port', 'invite', 'port,invite',
                       name='usersip_insecure',
                       metadata=Base.metadata))
    nat = Column(Enum('no', 'force_rport', 'comedia', 'force_rport,comedia',
                      name='usersip_nat',
                      metadata=Base.metadata))
    promiscredir = Column(Integer)
    usereqphone = Column(Integer)
    videosupport = Column(Enum('no', 'yes', 'always',
                               name='usersip_videosupport',
                               metadata=Base.metadata))
    trustrpid = Column(Integer)
    sendrpid = Column(String(16))
    allowsubscribe = Column(Integer)
    allowoverlap = Column(Integer)
    dtmfmode = Column(Enum('rfc2833', 'inband', 'info', 'auto',
                           name='usersip_dtmfmode',
                           metadata=Base.metadata))
    rfc2833compensate = Column(Integer)
    qualify = Column(String(4))
    g726nonstandard = Column(Integer)
    disallow = Column(String(100))
    allow = Column(Text)
    autoframing = Column(Integer)
    mohinterpret = Column(String(80))
    mohsuggest = Column(String(80))
    useclientcode = Column(Integer)
    progressinband = Column(Enum('no', 'yes', 'never',
                                 name='usersip_progressinband',
                                 metadata=Base.metadata))
    t38pt_udptl = Column(Integer)
    t38pt_usertpsource = Column(Integer)
    rtptimeout = Column(Integer)
    rtpholdtimeout = Column(Integer)
    rtpkeepalive = Column(Integer)
    deny = Column(String(31))
    permit = Column(String(31))
    defaultip = Column(String(255))
    setvar = Column(String(100), nullable=False, server_default='')
    host = Column(String(255), nullable=False, server_default='dynamic')
    port = Column(Integer)
    regexten = Column(String(80))
    subscribecontext = Column(String(80))
    fullcontact = Column(String(255))
    vmexten = Column(String(40))
    callingpres = Column(Integer)
    ipaddr = Column(String(255), nullable=False, server_default='')
    regseconds = Column(Integer, nullable=False, server_default='0')
    regserver = Column(String(20))
    lastms = Column(String(15), nullable=False, server_default='')
    parkinglot = Column(Integer)
    protocol = Column(enum.trunk_protocol, nullable=False, server_default='sip')
    category = Column(Enum('user', 'trunk',
                           name='useriax_category',
                           metadata=Base.metadata),
                      nullable=False)
    outboundproxy = Column(String(1024))
    transport = Column(String(255))
    remotesecret = Column(String(255))
    directmedia = Column(Enum('no', 'yes', 'nonat', 'update', 'update,nonat',
                           name='usersip_directmedia',
                           metadata=Base.metadata))
    callcounter = Column(Integer)
    busylevel = Column(Integer)
    ignoresdpversion = Column(Integer)
    session_timers = Column('session-timers',
                            Enum('originate', 'accept', 'refuse',
                                 name='usersip_session_timers',
                                 metadata=Base.metadata))
    session_expires = Column('session-expires', Integer)
    session_minse = Column('session-minse', Integer)
    session_refresher = Column('session-refresher',
                               Enum('uac', 'uas',
                                    name='usersip_session_refresher',
                                    metadata=Base.metadata))
    callbackextension = Column(String(255))
    registertrying = Column(Integer)
    timert1 = Column(Integer)
    timerb = Column(Integer)
    qualifyfreq = Column(Integer)
    contactpermit = Column(String(1024))
    contactdeny = Column(String(1024))
    unsolicited_mailbox = Column(String(1024))
    use_q850_reason = Column(Integer)
    encryption = Column(Integer)
    snom_aoc_enabled = Column(Integer)
    maxforwards = Column(Integer)
    disallowed_methods = Column(String(1024))
    textsupport = Column(Integer)
    commented = Column(Integer, nullable=False, server_default='0')
