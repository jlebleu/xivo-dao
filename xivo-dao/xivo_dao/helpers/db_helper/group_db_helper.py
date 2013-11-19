# -*- coding: UTF-8 -*-


from xivo_dao.alchemy.groupfeatures import GroupFeatures as GroupSchema
from xivo_dao.alchemy.queuemember import QueueMember as QueueMemberSchema
from xivo_dao.helpers.db_manager import daosession


@daosession
def get_group(session, group_id):
    row = (session.query(GroupSchema)
                  .filter(GroupSchema.id == group_id)
                  .first())

    return row if row else None


@daosession
def find_all_user_in_group_name(session, group_name):
    rows = (session.query(QueueMemberSchema.userid)
                   .filter(QueueMemberSchema.queue_name == group_name)
                   .filter(QueueMemberSchema.usertype == 'user')
                   .filter(QueueMemberSchema.category == 'group')
                   .all())

    return [row[0] for row in rows]
