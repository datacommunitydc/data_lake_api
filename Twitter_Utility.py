
# coding: utf-8

# In[7]:

# Python Twitter API 
# Authored By Elliott Miller - DataFighter
# twitter handle @datafighter1
# email: ellmill00@gmail.com

# I just like using pandas to parse and write things
import pandas as pd

# python-twitter library
# you can obtain this by using pip python-twitter
# documentation at https://pypi.python.org/pypi/python-twitter/
import twitter

# Create the api
# You need to input your own twitter keys and tokens
# You can get the keys by registering at https://apps.twitter.com/
api = twitter.Api(consumer_key='Input Your Own Consumer Key',
consumer_secret='Input Your Own Consumer Key',
access_token_key='Input your access token key',
access_token_secret='Input access token secret')

# Uncomment and run to verify your credentials
# print api.VerifyCredentials()

# Get all of the statuses. It Outputs to a list
statuses = api.GetUserTimeline(screen_name='DataCommunityDC')

# Uncomment the next line to print statuses
# print [s.text for s in statuses]

# ***The following two lines require pandas***

# make a pandas dataframe from the status array
df = pd.DataFrame(statuses)

# write the twitter statuses as a .csv file
# using pandas
df.to_json('Twitter.csv')
df.to_json('Twitter.json')

