
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

# python-twitter library
# you can obtain this by using pip python-twitter
# documentation at https://pypi.python.org/pypi/python-twitter/
import twitter

# library that makes requests easy to do
import requests
import ast
import decimal

# from config import *
from tem_config import *
API_KEY = API_KEYS['DC2']

API_ROOT = 'https://api.meetup.com/'
MEETUP_API_FAIL = 'Failed Response'

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

def GetGroupMembers(GroupID):
    '''
    Mimics the Meetup API endpoint: https://secure.meetup.com/meetup_api/console/?path=/2/members

    :param GroupID:
    :return:
    '''
    gid = GetGroupID(GroupID)

    endpoint = API_ROOT + "/2/members?key=" + API_KEY +"&group_id="+ str(gid)
    response = requests.get( endpoint )
    members = Eval_Response( response )
    return members

    # What do I want to do with this? I'd say the first step is just storing all this stuff so we can do whatever calls we want.

def GetGroupUpcomingEvents(GroupID):
    '''
    Will return events coming up, not old events.

    :param GroupID:
    :return:
    '''
    # http://www.meetup.com/meetup_api/docs/2/groups/
    gid = GetGroupID(GroupID)
    endpoint = API_ROOT + "2/events?key=" + API_KEY +"&group_id="+ str(gid)
    response = requests.get( endpoint )
    event_res = Eval_Response(response)
    return event_res

def GetGroupEvent(GroupID,EventID):

    gid = GetGroupID(GroupID)
    endpoint = API_ROOT + str(GroupID) + "/events/" + str(EventID)
    # https://api.meetup.com/dcnightowls/events/227458852?&sign=true&photo-host=public
    response = requests.get( endpoint )
    event_res = Eval_Response(response)
    return event_res

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

def GatherGroupData():

    group_data = {}
    group_members = {}
    group_reviews = {}
    group_events = {}
    for g,gurl in enumerate(DC2_PROGRAMS):
        group_data[gurl] = GetGroupOpenData(gurl)
        group_members[gurl] = GetGroupMembers(gurl)
        group_reviews[gurl] = GetGroupReviews(gurl)
        group_events[gurl] = GetGroupEvents(gurl)

    SaveGroupData(group_data)
    SaveMemberData(group_members)
    SaveGroupReviews(group_reviews)
    SaveGroupEvents(group_events)

def GetMemberEventData(MemberID,EventID):
    '''
    Created initially as part of ranking members for rsvp vs waitlist at events

    :param MemberID:
    :return:
    '''
    # http://www.meetup.com/meetup_api/docs/:urlname/events/:event_id/comments/#list - member
    response = requests.get( API_ROOT + "2/events/" + str(EventID) + "?key=" + API_KEY +"&group_id="+ str(gid))
    return member_group_data

def SaveGroupData(group_data):
    '''
    Save to S3 or a Mongo Database

    :param group_data:
    :return:
    '''

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

def CreateMemberConnections():
    '''
    Get data from DC2 S3/database and create member associations.
    There are lots of ways to associate two people, lets just list them all in a hash
    1. Attended same event
    2. Interested in the same topic
    3. Same Keywords (TFIDF of all DC2?)

    :return:
    '''

    gmems = GetGroupMembersDC2(gid)
    gmems_keys = gmems.keys()
    gmem_matrix = []
    for m1,gmem1 in enumerate(gmems_keys):
        for m2,gmem2 in enumerate(gmems_keys):
            # The goal is to show how members are connected in different ways, allowing for an organic search
            if True:
                gmem_matrix.append((m1,m2))

    return gmem_matrix

    # SaveMemberConnections()

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

def RankMemberByActivity(GroupName,EventID=None):
    '''
    Meetup events are challenged by their RSVP's because it's unclear who will show up when.
    Some venues, such as Chief, FI Consulting, Capital One Labs, etc., require a rsvp list to allow people in at the door.
    Some venues do not want to turn away people as it creates resentment to the organization.
    Ranking options could be:
      1. User's friends at local events: If the user is well connected, treat them well.
        > http://www.meetup.com/meetup_api/docs/2/member/#get - facebook_connection

      2. Number of active memberships: If the user is very active, keep them around.
        > http://www.meetup.com/meetup_api/docs/2/member/#get - membership_count

      3. Topics: If the user shares many of the same topics, they're likely to attend.
        > http://www.meetup.com/meetup_api/docs/2/member/#get - topics

      4. Active Member in Group: Do they check the message board? Read materials? Include them!
        > http://www.meetup.com/meetup_api/docs/:urlname/events/:event_id/comments/#list - member
        > http://www.meetup.com/meetup_api/docs/:urlname/#get - member_sample
        > http://www.meetup.com/meetup_api/docs/members/:member_id/#get - group_profile

    :param members:
    :return:
    '''

    gid = GetGroupID(GroupName)
    members = GetGroupMembers(gid)
    events = GetGroupEvents(gid)

    for event in events:
        edata = GetEventData(event['id'])
        eid = edata['']

    dc2members = {}
    for member in members:
        mid = member['id']
        dc2members[str(mid)] = {}

        mactive_count = member['membership_count']
        mtopics = member['topics']
        mname = member['name']
        mservices = member['other_services']

        mevent_data = GetMemberEventData(mid,eid)

        dc2members[str(mid)]['active_count'] = mactive_count
        dc2members[str(mid)]['topics'] = mtopics
        dc2members[str(mid)]['name'] = mname
        dc2members[str(mid)]['services'] = mservices
        dc2members[str(mid)]['event_data'] = mevent_data





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



