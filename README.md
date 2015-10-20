Code for making an API to contribute data to DC2's data lake

Running the Flask API Locally:

REQUIRED SERVICES

To run locally, you will need to have a redis server and amqp server running
and a celery worker with the adjunct to accept jobs.

On ubuntu 12.04 or later, simply run to install these services 
and begin running them on default ports.

sudo apt-get redis-server python-celery


DEPENDENCIES

Python packages required include:

flask
boto
redis
amqp
magic
xlrd

Install with:

sudo easy_install magic
sudo pip install Flask boto redis amqp xlrd

Note that several of these dependencies overlap with the adjunct processor.

Additionally, you will need the ThreeScalePY package which 
must be downloaded from github and installed manually. 
Clone this repository and follow instructions for setup:
https://github.com/3scale/3scale_ws_api_for_python

CONFIGURATION

Copy sample_config.py to config.py and alter the appropriate variables if necessary.

RUNNING

To run the api, type:

python api.py

This terminal will now display status messages from the API.

CALLING

The api will be running on your localhost with port 5000 by default. 

To call, use the following example curl calls with valid app_id and app_key pairs:

POST file data:
curl -i -F "app_id=12345EXAMPLE" -F "app_key=abc6943jqq509x26EXAMPLE" -F "file=@/path/to/1984_Excerpt.txt;type=text/plain" "http://127.0.0.1:5000/v1/documents"

GET the status of a job:
curl -i -X GET "http://127.0.0.1:5000/v1/documents/queue/f4d732ae-4264-40b5-9540-bf75f4799a76?app_id=12345EXAMPLE&app_key=abc6943jqq509x26EXAMPLE"

GET Twitter Data:
curl -i -X GET "http://127.0.0.1:5000/v1/documents/twitter/f4d732ae-4264-40b5-9540-bf75f4799a76?app_id=12345EXAMPLE&app_key=abc6943jqq509x26EXAMPLE&time_range=MMDDYYYY-MMDDYYYY"

GET the location of the result files:
curl -i -X GET "http://127.0.0.1:5000/v1/documents/f4d732ae-4264-40b5-9540-bf75f4799a76?app_id=12345EXAMPLE&app_key=abc6943jqq509x26EXAMPLE"

MONITORING

You can monitor the status of the API from either the terminal from which it was started OR by viewing the api.log file.

CHANGELOG
