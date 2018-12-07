
# Specify user file path for saved files
filepath = '/Users/ouliang/Google Drive/DRAGON/Data Preprocessing/Group Project/'


"""
###########################
    Acquire Yelp Data
###########################
"""

import requests

# Create request header for authorization
user_key = '5NczmeloT_5Qc8niaCRJfZRT5P83RIQces_05BZgQqzYZ8uO6LPDBNHtl59auUzg5ukvsdSFWHIJnwesgrp7NfSA-4Xvo1juZSH0IJsUK1SlNk7KhZEVet_-kwrAW3Yx'

from urllib.parse import quote

results = [] # results from daily queries are appended into a list for that day

def request(host, path, api_key, url_params):
    """
        Define a request function that constructs the url based on input parameters and return the results
    """
    url = '{0}{1}'.format(host, quote(path.encode('utf8'))) # use quote to escape special characters
    header = {'Authorization': 'Bearer %s' % api_key}

    print(u'Querying {0} ...'.format(url)) # print unicode display
    response = requests.request('GET', url, headers=header, params=url_params)
    return results.append(response.json())

def search(api_key, term, location, limit, sort_by, offset):
    """
        Define a search function for inputting paremeters
        "term" is for business type
    """
    my_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(', ', '+'),
        'limit': limit,
        'sort_by': sort_by,
        'offset': offset
    }
    return request(API_HOST, SEARCH_PATH, api_key, my_params)

## Define constant variables
API_HOST = 'http://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'

## Tune parameters where needed
business_type = 'restaurant'
sort_criteria = 'rating'
user_location = 'Philadelphia, PA'

import time
SEARCH_LIMIT = 50 # This is the max number of business results to return.
DAILY_CALLS = 20

def calls(location, api_key):
    """
        Set up the appropriate offset for each call.
        Each call returns 50 results, we need 20 calls to finish 1000 restaurants
    """
    calls = range(DAILY_CALLS)
    for call in calls:
        offset = call * SEARCH_LIMIT # An incremental call should add 50 more to the offset
        search(api_key, business_type, location, SEARCH_LIMIT, sort_criteria, offset)
        time.sleep(1) # Wait for a second between calls

# Create daily files in order to preserve previous results in case of errors being appended to the same file
import json
import datetime

today = datetime.date.today().strftime("%m%d%y")

def YelpJob():
    """ Drive function to make API calls to Yelp """
    calls(user_location,user_key)
    json.dump(results, open(filepath+'Yelp_'+today+'.json', 'w+'))

"""
##############################
     Getting weather data
##############################
"""

#OpenWeatherMap API key
user_owmKey = "ffc55dc8f3dd47ff5e138b730603d46a"
endpoint="http://api.openweathermap.org/data/2.5/weather?q=Philadelphia,us&APPID="+user_owmKey

def weatherJob():
    """ Acquire today's weather """
    weather = requests.get(endpoint)
    with open(filepath+'weather_'+today+'.json', 'a+') as f:
        json.dump(weather.json(),f)

# Run jobs
YelpJob()
weatherJob()
