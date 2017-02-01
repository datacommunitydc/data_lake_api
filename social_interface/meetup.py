
import requests


API_KEY = API_KEYS['DC2']

API_ROOT = 'https://api.meetup.com/'
MEETUP_API_FAIL = 'Failed Response'

DATA_DIRECTORY = "../data"

def GetGroupID(GroupName):
    '''
    Most people know the name, not the ID

    :param GroupName:
    :return:
    '''

    # Check to see if they gave the url string, if so then go get the numeric ID
    if isinstance(GroupName,basestring):
        # Try DC2 S3/Mongo first
        ### PLACEHOLDER ###
        endpoint = API_ROOT + GroupName + "?sign=true&key=" + API_KEY
        response = requests.get( endpoint )
        grp_res = Eval_Response( response )
        if grp_res==MEETUP_API_FAIL:
            gid = -1
        else:
            gid = grp_res['id']
    else:
        gid = GroupName

    return gid

# Takes in a group name and outputs a .json file that has the same name as the input parameter
# USe of this function will also require an api key
def GetGroupOpenData(GroupID):
    '''
    This function grabs key information about your group so additional calls can be made.
    API_KEY is a config parameter and must be kept private. You can get one from https://secure.meetup.com/meetup_api/key/

    :param GroupID: The end of the www.meetup.com/*** that gives the name of the group (e.g. Data-Visualization-DC)
    :return:
    '''

    gid = GetGroupID(GroupID)

    #This is simplified using the python requests library
    endpoint = API_ROOT + "/2/groups?key="+ API_KEY +"&group_id="+ str(gid)
    response = requests.get( endpoint )
    data_res = Eval_Response(response)
    return data_res

def GetGroupReviews(GroupID):

    gid = GetGroupID(GroupID)

    response = requests.get( API_ROOT + "comments?key=" + API_KEY +"&group_id="+ str(gid))
    return Eval_Response(response)

def Eval_Response(response):
    if (response.status_code >=200) & (response.status_code <= 299):
        return ujson.loads( response.text )
        # return ParseResponse(response.text)
        # return ast.literal_eval(response.text)
    else:
        return MEETUP_API_FAIL # Need error handling.

###########
###########

def GetEventRSVPs(EventID):
    '''
    Uses the RSVP endpoint, meant to rank everyone in an event (as opposed to the entire group)
    https://api.meetup.com/2/rsvps?&event_id=227834443

    :param EventID: if the name isn't descriptive enough, you shouldn't be coding.
    :return:
    '''
    if isinstance(EventID,int):
        endpoint = API_ROOT + "2/rsvps?&event_id=" + str(EventID)
        rsvp_res = Eval_Response( requests.get( endpoint ))
    else:
        rsvp_res = "Bad Event ID"

    return rsvp_res

#-----------------------------------------------------------------------------------------------------------------------

def GetGroupMembers(GroupID,OffsetLimit=1,Page=None):
    '''
    Mimics the Meetup API endpoint: https://secure.meetup.com/meetup_api/console/?path=/2/members

    :param GroupID: Either the urlname or numeric ID
    :param OffsetLimit: Tells meetup which index to begin pulling the next X members from
    :return:
    '''
    gid = GetGroupID(GroupID)

    endpoint = API_ROOT + "/2/members?key=" + API_KEY +"&group_id="+ str(gid)
    potentially_more = True
    offset = 0
    members = []
    while (potentially_more & (offset<OffsetLimit)):
        offpoint = endpoint + "&offset=" + str(offset)
        # if Page!=None:
        #     offpoint += "&page=" + str(Page)
        response = Eval_Response( requests.get( offpoint ))
        batch = response['results']
        if len(batch)>0:
            # We are currently not saving the meta data for expediency of development
            #   and because there is no immediate application.
            members += batch
            offset += 1
            if DEBUG:
                print("Offset = "+str(offset)+" More Members yet...")
        else:
            potentially_more = False
            if DEBUG:
                print("Done pulling the members!")
    return members

    # What do I want to do with this? I'd say the first step is just storing all this stuff so we can do whatever calls we want.

def SaveGroupMembers(group_url,OFFSET_LIMIT=1):
    '''
    Save to S3 or a Mongo Database

    :param group_data:
    :return:
    '''

    members = GetGroupMembers(group_url,OffsetLimit=OFFSET_LIMIT)

    SavePickle(members,'_api_2_members',group_url,PRINT="Saved Group Member Data")

    return members

def LoadGroupMembers(GroupURL,Directory='.'):
    '''
    These are placeholders right now, I imagine they may get more complicated.

    :param GroupURL:
    :param Directory:
    :return:
    '''
    return LoadAPI(str(GroupURL),Directory=Directory)

#-----------------------------------------------------------------------------------------------------------------------

def GetMemberGroups(MemberID):
    '''
    Initially used to determine the number of groups they're a member of versus the number they're active in
    :param MemberID:
    :return:
    '''
    # https://api.meetup.com/members/12511409?&sign=true&photo-host=public&fields=memberships&page=20
    endpoint = API_ROOT + "members/" + str(MemberID) + "?fields=memberships"
    event_res = Eval_Response( requests.get( endpoint ))
    return event_res

def SaveMemberGroups(MemberID):
    '''
    Save to S3 or a Mongo Database

    :param group_data:
    :return:
    '''

    groups = GetMemberGroups(MemberID)

    SavePickle(groups,'_api_members_id_memberships',MemberID,PRINT="Saved Member Group Data")

    return groups

def LoadMemberGroups(MemberID,Directory='.'):
    '''
    We need to load everything and save it before sciencing it.

    :param MemberID:
    :return:
    '''

    return LoadAPI(str(MemberID),Directory=Directory)

#-----------------------------------------------------------------------------------------------------------------------

def GetGroupEvents(GroupID,Time=-1,Status=None):
    '''

    :param GroupID: url or id of the meetup group
    :param Time: string or array:
        string may have one number (e.g. 9), or string may be two numbers (e.g. 0,9)
        array may have length 1 or 2.
            Length 1 contains a string (e.g. 0,9),
            Length 2 contains begin and end time in milliseconds since epoch [0,9] NO DECIMALS!
    :param Status:
    :return:
    '''
    # http://www.meetup.com/meetup_api/docs/2/groups/
    gid = GetGroupID(GroupID)
    endpoint = API_ROOT + "2/events?key=" + API_KEY +"&group_id="+ str(gid)
    if ((Status!=None) & (Time!=-1)):
        endpoint += "&time=" + str(Time[0])
        if len(Time)>1:
            endpoint += "," + str(int(Time[1]))
        endpoint += "&status=" + str(Status)
    event_res = Eval_Response( requests.get( endpoint ))
    return event_res

def GetGroupEvent(GroupID,EventID):

    gid = GetGroupID(GroupID)
    endpoint = API_ROOT + str(GroupID) + "/events/" + str(EventID)
    # https://api.meetup.com/dcnightowls/events/227458852?&sign=true&photo-host=public
    response = requests.get( endpoint )
    event_res = Eval_Response(response)
    return event_res

#-----------------------------------------------------------------------------------------------------------------------

def GetMemberEventRSVPs(MemberID,Time=-1,Status=None):
    # https://api.meetup.com/2/events?&sign=true&photo-host=public&group_id=6957082&member_id=12511409&time=0,1450815009391&status=past
    endpoint = API_ROOT + "2/events?member_id=" + str(MemberID)
    if ((Status!=None) & (Time!=-1)):
        endpoint += "&time=" + str(Time[0])
        if len(Time)>1:
            endpoint += "," + str(int(Time[1]))
        endpoint += "&status=" + str(Status)
    rsvps = Eval_Response( requests.get( endpoint ))
    return rsvps

def SaveMemberEventRSVPs(MemberID,Time=-1,Status=None):
    '''
    Save to S3 or a Mongo Database

    :param group_data:
    :return:
    '''

    rsvps = GetMemberEventRSVPs(MemberID,Time=-1,Status=Status)

    SavePickle(rsvps, '_api_2_events',MemberID,PRINT="Saved Member Event RSVPs")

    return rsvps

def LoadMemberEventRSVPs(MemberID,Directory='.'):
    '''
    These are placeholders right now, I imagine they may get more complicated.

    :param GroupURL:
    :param Directory:
    :return:
    '''
    return LoadAPI(str(MemberID),Directory=Directory)

#-----------------------------------------------------------------------------------------------------------------------

def GetMemberData(MemberID):
    # 1. User's friends at local events: If the user is well connected, treat them well.
    #   > http://www.meetup.com/meetup_api/docs/2/member/#get - facebook_connection
    # Endpoint: https://api.meetup.com/2/member/146282552
    endpoint = API_ROOT + "2/member/" + str(MemberID) + "?key=" + API_KEY
    response = requests.get( endpoint )
    mem_res = Eval_Response(response)
    return mem_res

# def SaveMemberData(MemberID):
# def LoadMemberData(MemberID):

#-----------------------------------------------------------------------------------------------------------------------

def GetGroupMemberComments(GroupID,MemberID=None):

    # GET String
    if isinstance(GroupID,str):
        GroupID = GetGroupID(GroupID)

    endpoint = API_ROOT + "/2/event_comments?key=" + API_KEY + "&group_id=" + str(GroupID)
    if MemberID!=None:
        endpoint += "&member_id=" + str(MemberID)
    response = requests.get( endpoint )
    comment_res = Eval_Response(response)
    return comment_res

def SaveGroupMemberComments(GroupID,MemberID=None):

    comment_res = GetGroupMemberComments(GroupID,MemberID=MemberID)

    file_string = str(GroupID) + '_' + str(MemberID)
    SavePickle(comment_res, '_api_2_event_comments',file_string,PRINT="Saved Group Member Comments")

    return comment_res

def LoadGroupMemberComments(GroupID,MemberID=None,Directory='.'):
    file_string = str(GroupID) + '_' + str(MemberID)
    return LoadAPI(file_string,Directory=Directory)

#-----------------------------------------------------------------------------------------------------------------------

def GetMemberEventData(MemberID,EventID):
    '''
    Collecting member event data to know their RSVP status and others'...

    :param MemberID:
    :return:
    '''
    # https://api.meetup.com/2/events?member_id=12251810&offset=0&format=json&limited_events=False&event_id=227834443&photo-host=public&page=500&fields=&order=time&desc=false&status=upcoming&sig_id=12251810&sig=653cac1d573b590a6889cef2e9a3433ea8ff1576
    response = requests.get( API_ROOT + "2/events?key=" + API_KEY + "&member_id=" + str(MemberID) + "&event_id=" + str(EventID))
    return response
