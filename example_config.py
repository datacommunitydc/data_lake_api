#!/usr/bin/env python 2
"""Configuration variables for the DC2 Data Lake API."""

REDISHOST = "127.0.0.1"
REDISPORT = 9999 # create one
AWSKEY = "" 
AWSSECRET = ""
S3ENDPOINT = "s3.amazonaws.com"
BUCKET = your amazon bucket name
RMQHOST = "127.0.0.1"
RMQPORT = 999 # different than REDISPORT
RMQUSERNAME = "guest"
RMQVHOST = "/"
RMQPASSWORD = "guest"
RMQEXCHANGE = "dc2_data_lake.jobs.input"
THREESCALEKEY = <your threescale key>
SUPPORTEMAIL = "info@datacommunitydc.org"
LOGFILE = "api.log"
FLASKPORT = 9999 # DIFFERENT THAN REDIS OR RMQPORT
