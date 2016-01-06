
# coding: utf-8

# In[13]:

# Python Twitter API 
# Authored By Elliott Miller - DataFighter
# twitter handle @datafighter1
# email: ellmill00@gmail.com

# I just like using pandas to parse and write things
# This 
import pandas as pd

# Will also use the json library. 
import json
import ujson
import uuid
import cPickle as pkl
import os
import time

# python-twitter library
# you can obtain this by using pip python-twitter
# documentation at https://pypi.python.org/pypi/python-twitter/
import twitter

# library that makes requests easy to do
import requests
import ast
import decimal

from datetime import datetime

import numpy as np

# from config import *
from tem_config import *
API_KEY = API_KEYS['DC2']

API_ROOT = 'https://api.meetup.com/'
MEETUP_API_FAIL = 'Failed Response'

#====================================================================================================
# BEGIN ENDPOINT FUNCTIONS BEGIN ENDPOINT FUNCTIONS BEGIN ENDPOINT FUNCTIONS BEGIN ENDPOINT FUNCTIONS
#====================================================================================================
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

def ParseResponse(source):

    # source = "(Decimal('11.66985'), Decimal('1e-8'),"\
    #     "(1,), (1,2,3), 1.2, [1,2,3], {1:2})"

    tree = ast.parse(source, mode='eval')

    # using the NodeTransformer, you can also modify the nodes in the tree,
    # however in this example NodeVisitor could do as we are raising exceptions
    # only.
    class Transformer(ast.NodeTransformer):
        ALLOWED_NAMES = set(['Decimal', 'None', 'False', 'True'])
        ALLOWED_NODE_TYPES = set([
            'Expression', # a top node for an expression
            'Tuple',      # makes a tuple
            'Call',       # a function call (hint, Decimal())
            'Name',       # an identifier...
            'Load',       # loads a value of a variable with given identifier
            'Str',        # a string literal

            'Num',        # allow numbers too
            'List',       # and list literals
            'Dict',       # and dicts...
        ])

        def visit_Name(self, node):
            if not node.id in self.ALLOWED_NAMES:
                raise RuntimeError("Name access to %s is not allowed" % node.id)

            # traverse to child nodes
            return self.generic_visit(node)

        def generic_visit(self, node):
            nodetype = type(node).__name__
            if nodetype not in self.ALLOWED_NODE_TYPES:
                raise RuntimeError("Invalid expression: %s not allowed" % nodetype)

            return ast.NodeTransformer.generic_visit(self, node)


    transformer = Transformer()

    # raises RuntimeError on invalid code
    transformer.visit(tree)

    # compile the ast into a code object
    clause = compile(tree, '<AST>', 'eval')

    # make the globals contain only the Decimal class,
    # and eval the compiled object
    result = eval(clause, dict(Decimal=decimal.Decimal))

    print(result)
    return result

#====================================================================================================
# BEGIN S3 SAVING BEGIN S3 SAVING BEGIN S3 SAVING BEGIN S3 SAVING BEGIN S3 SAVING BEGIN S3 SAVING
#====================================================================================================

def SavePickle(save_data,endpoint_string,endpoint_input,PRINT='Saved Data'):
    '''
    Each of the endpoints needs to pickle the data is a similar way.

    :return:
    '''

    result = False
    id = str(uuid.uuid1())
    filename = str(endpoint_input) + str(endpoint_string) + '.' + id + '.pkl'
    f = file(filename,'wb')
    pkl.dump(save_data,f,protocol=pkl.HIGHEST_PROTOCOL)
    f.close()
    if DEBUG:
        print(PRINT)

    result = True # asserting the save will make this conditional
    return result

def LoadPickle(filename):
    f = file(filename,'rb')
    data = pkl.load(f)
    return data

def LoadAPI(keyword,Directory='.'):
    '''
    We need to load everything and save it before sciencing it.

    :param MemberID:
    :return:
    '''

    files = os.listdir(Directory)
    potential_files = []
    for filename in files:
        if keyword in filename:
            potential_files += [filename]

    # If something matched the keyword, load the latest one.
    if len(potential_files)>0:
        best_time = 0
        for this in potential_files:
            mod_time = time.ctime(os.path.getmtime(this))
            if mod_time > best_time:
                best_time = mod_time
                load_this = this
            # print "last modified: %s" % time.ctime(os.path.getmtime(file))
            # print "created: %s" % time.ctime(os.path.getctime(file))

    data = LoadPickle(load_this)
    return data

def SaveMemberData(group_members):
    '''
    Save to S3 or a Mongo Database

    :param group_members:
    :return:
    '''

def SaveGroupReviews(group_reviews):
    '''
    Save to S3 or a Mongo Database

    :param group_reviews:
    :return:
    '''

def SaveGroupEvents(group_events):
    '''
    Save to S3 or a Mongo Database

    :param group_reviews:
    :return:
    '''

#====================================================================================================
# END S3 SAVING END S3 SAVING END S3 SAVING END S3 SAVING END S3 SAVING END S3 SAVING
#====================================================================================================

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
    We are currently not saving the meta data for expediency of development
        and because there is no immediate application.

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
    Created initially as part of ranking members for rsvp vs waitlist at events

    :param MemberID:
    :return:
    '''
    # http://www.meetup.com/meetup_api/docs/:urlname/events/:event_id/comments/#list - member
    response = requests.get( API_ROOT + "2/events/" + str(EventID) + "?key=" + API_KEY +"&group_id="+ str(gid))
    return response

#====================================================================================================
# END ENDPOINT FUNCTIONS END ENDPOINT FUNCTIONS END ENDPOINT FUNCTIONS END ENDPOINT FUNCTIONS
#====================================================================================================
# BEGIN AGGREGATION FUNCTIONS BEGIN AGGREGATION FUNCTIONS BEGIN AGGREGATION FUNCTIONS
#====================================================================================================

# def GatherGroupData():
#
#     group_data = {}
#     group_members = {}
#     group_reviews = {}
#     group_events = {}
#     for g,gurl in enumerate(DC2_PROGRAMS):
#         group_data[gurl] = GetGroupOpenData(gurl)
#         group_members[gurl] = GetGroupMembers(gurl)
#         group_reviews[gurl] = GetGroupReviews(gurl)
#         group_events[gurl] = GetGroupEvents(gurl)
#
#     SaveGroupData(group_data)
#     SaveMemberData(group_members)
#     SaveGroupReviews(group_reviews)
#     SaveGroupEvents(group_events)
#
# def CreateMemberConnections():
#     '''
#     Get data from DC2 S3/database and create member associations.
#     There are lots of ways to associate two people, lets just list them all in a hash
#     1. Attended same event
#     2. Interested in the same topic
#     3. Same Keywords (TFIDF of all DC2?)
#
#     :return:
#     '''
#
#     gmems = GetGroupMembersDC2(gid)
#     gmems_keys = gmems.keys()
#     gmem_matrix = []
#     for m1,gmem1 in enumerate(gmems_keys):
#         for m2,gmem2 in enumerate(gmems_keys):
#             # The goal is to show how members are connected in different ways, allowing for an organic search
#             if True:
#                 gmem_matrix.append((m1,m2))
#
#     return gmem_matrix
#
#     # SaveMemberConnections()

#-----------------------------------------------------------------------------------------------------------------------

def GatherMemberActivityData(GroupURL):
    '''
    We are gathering member data, but starting with the GropuURL. This has to do with the
    group focus of the ranking algorithm.
    In general, we are gathering data based on the service or algorithm that data supports.
        If we tried to download all data from all endpoints we would be reconstructing the
         Meetup.com API database, which is crazy.

    :param GroupURL:
    :return:
    '''

    epoch = datetime.utcfromtimestamp(0)
    now = datetime.utcnow()
    from_epoch = (now-epoch).total_seconds() *1000

    members = SaveGroupMembers(GroupURL,OFFSET_LIMIT=99999999999)
    # members = LoadGroupMembers(GroupURL)
    SaveGroupMemberComments(GroupURL)
    for member in members:
        mid = member['id']
        SaveMemberGroups(mid)
        SaveMemberEventRSVPs(mid,Time=[0,from_epoch],Status="past")

    print("Member Activity Data Saved.")

def RankMemberByActivity(GroupName,Test=False):
    '''
    Meetup events are challenged by their RSVP's because it's unclear who will show up when.
    Some venues, such as Chief, FI Consulting, Capital One Labs, etc., require a rsvp list to allow people in at the door.
    Some venues do not want to turn away people as it creates resentment to the organization.
    Ranking options could be:
      1. User's friends at local events: If the user is well connected, treat them well.
        > http://www.meetup.com/meetup_api/docs/2/member/#get - facebook_connection
        > FAIL: facebook_connection, if it is returned, only gives status.

      2. Number of active memberships: If the user is very active, keep them around.
        > http://www.meetup.com/meetup_api/docs/2/member/#get - membership_count

      3. Topics: If the user shares many of the same topics, they're likely to attend.
        > http://www.meetup.com/meetup_api/docs/2/member/#get - topics

      4. Active Member in Group: Do they check the message board? Read materials? Include them!
        > http://www.meetup.com/meetup_api/docs/:urlname/events/:event_id/comments/#list - member
        > http://www.meetup.com/meetup_api/docs/:urlname/#get - member_sample
        > http://www.meetup.com/meetup_api/docs/members/:member_id/#get - group_profile

      5. First time: If this is their first RSVP, let'em in

      6. Have they ever contributed money? let'em in!!

    :param members:
    :return:

    Note: Perhaps use meetup api batch processing?
    '''

    gid = GetGroupID(GroupName)

    # Calculations can not also be calling the meetup api, it's just too inefficient.
    members = LoadGroupMembers(GroupName)
    # members = GetGroupMembers(gid,OffsetLimit=1,Page=3)

    mem_vec = CalcMemberVector(members,gid)

    # topic_matrix = CalcTopicAssociations(mem_vec)
    group_matrix = CalcGroupAssociations(mem_vec)
    import matplotlib.pyplot as plt
    # plt.matshow(topic_matrix)
    plt.matshow(group_matrix)

    # Rank the members using the member-vector and association matrices
    # First cut people with no photo or no title

def CalcMemberVector(members,gid):
    '''
    The Member Vector is all the information pertinent to the Member ranking algroithm. It consists of:
    1. Member's comments at events
    2. Number of Active Groups
    3. Number of common Groups
    4. Number of common Topics
    5. Number of RSVP's
    6. Meetup active status

    :param members:
    :param gid:
    :return:
    '''

    epoch = datetime.utcfromtimestamp(0)
    now = datetime.utcnow()
    from_epoch = (now-epoch).total_seconds() *1000

    mem_vec = {}

    # mem_comments = GetGroupMemberComments(gid)
    mem_comments = LoadGroupMemberComments(gid)
    if DEBUG:
        print("Got Member Comments")

    for member in members:
        meys = member.keys()
        mid = member['id']
        mem_vec[mid] = {}

        # Do they participate in recent event conversations?
        mem_vec[mid]['status'] = member['status']
        mem_vec[mid]['commented'] = 0
        for comment in mem_comments['results']:
            if mid == comment['member_id']:
                mem_vec[mid]['commented'] += 1
                if mem_vec[mid]['commented'] >=3:
                    break

        # Membership count gives the number of groups they're active in
        if "membership_count" in meys:
            mem_vec[mid]['membership_count'] = member['membership_count']
        else:
            mem_vec[mid]['membership_count'] = 0

        # How many common groups?
        # https://secure.meetup.com/meetup_api/console/?path=/members/:member_id
        # moups = GetMemberGroups(mid)
        moups = LoadMemberGroups(mid)
        if DEBUG:
            print("Got member Groups")
        mgkeys = moups.keys()
        if "memberships" in mgkeys:
            mem_vec[mid]['groups'] = {'id':[],'urlname':[],'organizer':[]} # Initialize

            # Distinguish between Organizer and Member
            organizer_member = moups['memberships'].keys()
            if "organizer" in organizer_member:
                # PUT SOME VALUE HERE SO I SIDESTEP A GROUP ASSOCIATION MATRIX BECAUSE ORGANIZERS ARE AWESOME??
                memberships = moups["memberships"]["organizer"]
                mem_vec[mid]['groups']['id'] += [group['group']['id'] for group in memberships]
                mem_vec[mid]['groups']['urlname'] += [group['group']['id'] for group in memberships]
                mem_vec[mid]['groups']['organizer'] += [True] * len(memberships)

            if "member" in organizer_member:
                memberships = moups["memberships"]["member"]
                mem_vec[mid]['groups']['id'] += [group['group']['id'] for group in memberships]
                mem_vec[mid]['groups']['urlname'] += [group['group']['id'] for group in memberships]
                mem_vec[mid]['groups']['organizer'] += [False] * len(memberships)

        # How many common topics? So much easier than the groups...
        mem_vec[mid]['topics'] = member['topics']

        # Have they RSVP'd to any events?
        mem_rsvps = GetMemberEventRSVPs(mid,Time=[0,from_epoch],Status="past")
        print("Got member events")
        mem_vec[mid]['rsvps'] = 0
        for event in mem_rsvps['results']:
            if event['group']['id'] == gid:
                mem_vec[mid]['rsvps'] += 1
                if mem_vec[mid]['rsvps'] >=3:
                    break

        # MONEY HONEY!! MONEY HONEY!! MONEY HONEY!! MONEY HONEY!! MONEY HONEY!! MONEY HONEY!!
        # MONEY HONEY!! MONEY HONEY!! MONEY HONEY!! MONEY HONEY!! MONEY HONEY!! MONEY HONEY!!
        # This is a part of the user's group profile, and membership dues are tracked, but contributions are not.
        # https://secure.meetup.com/meetup_api/console/?path=/2/profile/:gid/:mid
        # TO GET CONTRIBUTIONS, WE WOULD HAVE TO SCRAPE THIS PAGE:
        #             http://www.meetup.com/dcnightowls/money/

    return mem_vec

def CalcGroupAssociations(mem_vec):

    mids = mem_vec.keys()
    num_mems = len(mids)
    group_matrix = np.zeros([num_mems,num_mems])
    for r,midr in enumerate(mids):
        print("Member #" + str(midr))
        for c,midc in enumerate(mids):
            if (c>r) & ('groups' in mem_vec[midr]) & ('groups' in mem_vec[midc]):
                # Intersection of common topics
                group_matrix[r,c] = len(np.intersect1d( np.array(mem_vec[midr]['groups']['id']),
                                                        np.array(mem_vec[midc]['groups']['id'])))
            else:
                group_matrix[r,c] = 0

    return group_matrix

def CalcTopicAssociations(mem_vec):

    mids = mem_vec.keys()
    num_mems = len(mids)
    topic_matrix = np.zeros([num_mems,num_mems]) # [[0 for x in range(num_mems)] for y in range(num_mems)]
    for r,midr in enumerate(mids):
        for c,midc in enumerate(mids):
            if c>r:
                # Intersection of common topics
                topic_matrix[r,c] = len(np.intersect1d( np.array(mem_vec[midr]['topics']),
                                                        np.array(mem_vec[midc]['topics'])))
            else:
                topic_matrix[r,c] = 0

    return topic_matrix

#=======================================================================================================================
# ENOUGH CALCULATING, ACT! ENOUGH CALCULATING, ACT! ENOUGH CALCULATING, ACT! ENOUGH CALCULATING, ACT! ENOUGH CALCULATING, ACT!
# ENOUGH CALCULATING, ACT! ENOUGH CALCULATING, ACT! ENOUGH CALCULATING, ACT! ENOUGH CALCULATING, ACT! ENOUGH CALCULATING, ACT!
#=======================================================================================================================

def RankMemberByKeyword(topic):
    '''
    When we search for a subject, we are interested in people that:
    1. Attend events with that topic
    2. Attend events we attend
    3. Have the topic in Meetup topics
    4. Have the topic in Group Description or Overall Description

    :param keyword:
    :return:
    '''

def GroupCommentWordCloud(GroupID,TFIDF=False):
    '''
    Calculate the frequency of each word for all of a group's events.

    :param GroupID:
    :param TFIDF:
    :return:
    '''

def RankEventRSVPs(EventID):
    '''
    Take the results of the member rankings and apply them to a specific event.

    :param EventID:
    :return:
    '''

    # get the members' ranks, update the event with the right key.
    # NONE OF THESE ARE WRITTEN YET!!!
    rsvps = GetEventRSVPs(EventID)
    mids = ExtractRSVPmembers(rsvps)
    ranking = GetMemberRanking(mids)

def CleanGroupMemberships(GroupID):
    '''
    So many people sign up and ultimately do nothing. They skew the stats, bootem.

    :param GroupID:
    :return:
    '''

#=======================================================================================================================
# This Function takes in a parameter as a screenname and then writes a json file
# With the screenname as the filename
def WriteTwitterStatuses(ScreenName):
    
    # Create the api
    # You need to input your own twitter keys and tokens
    # You can get the keys by registering at https://apps.twitter.com/
    api = twitter.Api(consumer_key='8gRwMGxYZalCX7L4LPumptrX4',
    consumer_secret='UXoLUMYjviNaRtICmufCnmxwQbL8iZLW0lPlqkVfysuQe16JO2',
    access_token_key='3302331191-oLc2rATkPxglx9tLnKWh1lEemgAurbXV20HltgP',
    access_token_secret='tcjqLjsCflhK5VFR16dVF4LPvCIzZPtvHJVX91rGMH5Ps')
    
    # Get all of the statuses. It Outputs to a list
    statuses = api.GetUserTimeline(screen_name = ScreenName)

    # ***The following two lines require pandas***    

    # make a pandas dataframe from the status array    
    df = pd.DataFrame(statuses)
    
    # write the twitter statuses as a .json file
    # using pandas    
    # The File Name is just the screenname
    df.to_json(str(ScreenName)+'.json')
    
    # Uncomment the next line to print statuses
    # print [s.text for s in statuses]
    
# Uncomment the next line and run to verify your credentials on Twitter:
# print api.VerifyCredentials()


# In[9]:




# In[11]:

# Takes in a group name and outputs a .json file that has the same name as the input parameter
# USe of this function will also require an api key
def WriteMeetupEvents(GroupName):
    #Put in your API key here
    #You can get one from https://secure.meetup.com/meetup_api/key/
    api_key = "5db37233e5711225b62251680323943"
    
    #Get request for the events list of a group
    #This is simplified using the python requests library
    response = requests.get("https://api.meetup.com/2/events?key=5db37233e5711225b62251680323943&group_urlname="+GroupName+"&sign=true")
    
    #Write the server respons as a json
    #This is unparsed. 
    with open(GroupName+'.json', 'w') as fp:
        json.dump(response.json(), fp)


# In[14]:

WriteMeetupEvents('Data-Community-DC')


# In[ ]:



