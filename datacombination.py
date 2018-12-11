# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 17:43:45 2018

@author: AkshayJk
"""

import pandas as pd
import os

def combine_restaurant():
    '''
    This is used to combine the restaurant data of all 4 cities and also include a new column to 
   recognize which city that restaurant belongs to
   '''
    results = pd.DataFrame([])
    fileList = []
    for fileObj in os.walk("."):
        fileList = fileObj[2]
        break
    for file in fileList:
        if "restaurant_data" in file:
            restaurant = pd.read_csv(file, skiprows = 0)
            city = (file.replace("restaurant_data_", "")).replace(".csv", "")
            if city == 'PHL':
                restaurant['City'] = 'Philadelphia'
            elif city == 'CHI':
                restaurant['City'] = 'Chicago'
            elif city == 'SFO':
                restaurant['City'] = 'San Francisco'
            else:
                restaurant['City'] = city
            restaurant.sort_values('date_id')
            print(restaurant[:10])
            results = results.append(restaurant)        
    results.to_csv("rest_data_combined.csv")
    
def combine_weather():
    '''
    This is used to combine the weather data of all 4 cities.
    '''
    results = pd.DataFrame([])
    fileList = []
    for fileObj in os.walk("."):
        fileList = fileObj[2]
        break
    for file in fileList:
        if "weather_data" in file:
            restaurant = pd.read_csv(file, skiprows = 0)
            restaurant.sort_values('date_id')
            print(restaurant[:10])
            results = results.append(restaurant)        
    results.to_csv("weat_data_combined.csv")

combine_restaurant()
combine_weather()
