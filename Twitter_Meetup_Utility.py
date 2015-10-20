
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

# python-twitter library
# you can obtain this by using pip python-twitter
# documentation at https://pypi.python.org/pypi/python-twitter/
import twitter

# library that makes requests easy to do
import requests
import ast

from config import *


def GetGroupID(GroupID):
    '''
    Most people know the name, not the ID

    :param GroupName:
    :return:
    '''

    # Check to see if they gave the url string, if so then go get the numeric ID
    if isinstance(GroupID,basestring):
        # Try DC2 S3/Mongo first
        ### PLACEHOLDER ###
        response = requests.get( API_ROOT + GroupID + "?key=" + API_KEY)
        grp_res = Eval_Response(response)
        gid = grp_res['id']
    else:
        gid = GroupID

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
    response = requests.get( API_ROOT + "2/groups?key="+ API_KEY +"&group_id="+ str(gid))
    return Eval_Response(response)

def GetGroupReviews(GroupID):

    gid = GetGroupID(GroupID)

    response = requests.get( API_ROOT + "comments?key=" + API_KEY +"&group_id="+ str(gid))
    return Eval_Response(response)

def Eval_Response(response):
    if (response.status_code >200) & (response.status_code < 299):
        return ast.literal_eval(response.text)
    else:
        return "Failed Response" # Need error handling.

def GetGroupMembers(GroupID):
    '''
    Mimics the Meetup API endpoint: https://secure.meetup.com/meetup_api/console/?path=/2/members

    :param GroupID:
    :return:
    '''
    gid = GetGroupID(GroupID)

    response = requests.get( API_ROOT + "2/members?key=" + API_KEY +"&group_id="+ str(gid))
    members = Eval_Response(response)

    # What do I want to do with this? I'd say the first step is just storing all this stuff so we can do whatever calls we want.

def GetGroupEvents(GroupID):

    gid = GetGroupID(GroupID)
    response = requests.get( API_ROOT + "2/events?key=" + API_KEY +"&group_id="+ str(gid))
    return Eval_Response(response)

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
    Get data from DC2 S3/database and create member associations

    :return:
    '''

    gmems = GetGroupMembersDC2(gid)
    gmems_keys = gmems.keys()
    for m1,gmem1 in enumerate(gmems_keys):
        for m2,gmem2 in enumerate(gmems_keys):
            # There are lots of ways to associate two people, lets just list them all in a hash
            # 1. Attended same event
            # 2. Interested in the same topic
            # 3. Same Keywords (TFIDF of all DC2?)

def RankMemberByKeyword(keyword):
    '''
    When we search

    :param keyword:
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



