from Twitter_Meetup_Utility import *
GroupName = "Data-Visualization-DC"
gid         = GetGroupID(GroupName)
comment_res = GetGroupMemberComments(gid)
data_res    = GetGroupOpenData(gid)
mem_res     = GetGroupMembers(gid)
gevent_res  = GetGroupUpcomingEvents(gid)
event_res   = GetGroupEvent(GroupName,"226826728")