from Twitter_Meetup_Utility import *
GroupName = "Data-Visualization-DC"
# MemberID = "146282552"
# gid         = GetGroupID(GroupName)
# # comment_res = GetGroupMemberComments(gid)
# # data_res    = GetGroupOpenData(gid)
# grpmem_res  = GetGroupMembers(gid,OffsetLimit=2)
#
# epoch = datetime.utcfromtimestamp(0)
# now = datetime.utcnow()
# from_epoch = (now-epoch).total_seconds() *1000
# gevent_res  = GetGroupEvents(gid,[0,from_epoch],Status="past")
# # event_res   = GetGroupEvent(GroupName,"226826728")
#
# MemberID = grpmem_res[0]['id']
# mem_res = GetMemberData(MemberID)

# GatherMemberActivityData(GroupName)
RankMemberByActivity(GroupName,Test=True)

# SaveGroupMembers(GroupName,OFFSET_LIMIT=100)