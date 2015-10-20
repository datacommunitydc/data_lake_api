#!/usr/bin/env python 2
"""Configuration variables for the DC2 Data Lake API."""

REDISHOST = "127.0.0.1"
REDISPORT = 9999 # create one
# AWSKEY = "AKIAJBKDBVYNHG3SQE6Q"
# AWSSECRET = "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"
AWSKEY = "AKIAITPGB7FS5V5US72A"
AWSSECRET = "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"
S3ENDPOINT = "s3.amazonaws.com"
BUCKET = "data-lake-test"
RMQHOST = "127.0.0.1"
RMQPORT = 999 # different than REDISPORT
RMQUSERNAME = "guest"
RMQVHOST = "/"
RMQPASSWORD = "guest"
RMQEXCHANGE = "dc2_data_lake.jobs.input"
THREESCALEKEY = <your threescale key> # Waiting on app authorization
SUPPORTEMAIL = "info@datacommunitydc.org"
LOGFILE = "api.log"
FLASKPORT = 9999 # DIFFERENT THAN REDIS OR RMQPORT
