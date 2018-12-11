# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 15:42:11 2018

@author: AkshayJk
"""
'''
Firstly, please download all your respective files to local host. I am not sure if this would work in
iPython notebook.
'''

import json
import csv
import pprint as pp
import os

def jsonToCSV_weather(filename):
    with open(filename, "r") as jsonfile:
        weather_data = json.load(jsonfile)
        pp.pprint(weather_data)
        final_dict = dict()
        simple_column = ['dt', 'visibility', 'id', 'name']
        compound_column = {'coords':['lon', 'lat'], 'wind':['speed', 'deg'], 'sys':['sunrise', 'sunset'], 'clouds':['all'], 'weather':['main', 'description'], 'main':['humidity', 'pressure', 'temp', 'temp_max', 'temp_min']}
        number_list = [s for s in filename if s.isdigit()]
        date_id = ""
        for number in number_list:
            date_id += number
        final_dict['date_id'] = date_id
        for column in weather_data:
            if column in simple_column:
                final_dict[column] = weather_data[column]
            elif column in compound_column:
                for c in compound_column:
                    if c == column:
                        if c == 'weather':
                            for categ in weather_data[column][0]:
                                if categ in compound_column[column]:
                                    final_dict[c + "_" + categ] = weather_data[column][0][categ]
                        else:
                            for categ in weather_data[column]:
                                if categ in compound_column[c]:
                                    final_dict[c + "_" + categ] = weather_data[column][categ]
        return final_dict
    
def jsonToCSV_yelp(filename):
    with open(filename, "r") as jsonfile:
        yelp_data = json.load(jsonfile)
        total_list = []
        number_list = [s for s in filename if s.isdigit()]
        date_id = ""
        for number in number_list:
            date_id += number
        simple_column = ['id', 'name', 'is_closed', 'url', 'review_count', 'rating', 'transactions', 'price', 'display_phone', 'distance']
        compound_column = {'categories':['alias'], 'coordinates':['latitude', 'longitude'], 'location':['display_address'] }
        count = 0
        for data in yelp_data:
            for dict_data in data['businesses']:
                count += 1
                final_dict = dict()
                final_dict['date_id'] = date_id
                for tag in dict_data:
                    if tag in simple_column:
                        if tag == 'transactions':
                            if len(dict_data[tag]) == 0:
                                final_dict[tag] = "N/A"
                            else:
                                final_dict[tag] = dict_data[tag]
                        else:
                            final_dict[tag] = dict_data[tag]
                    elif tag in compound_column:
                        for categ in dict_data[tag]:
                            if tag == 'categories':
                                for c in categ:
                                    if c in compound_column[tag]:
                                        if tag in final_dict:
                                            final_dict[tag] += " " + categ[c]
                                        else:
                                            final_dict[tag] = categ[c]
                            elif tag == 'location':
                                if categ in compound_column[tag]:
                                    final_dict[categ] = dict_data[tag][categ]
                            else:
                                for categ in dict_data[tag]:
                                    final_dict[categ] = dict_data[tag][categ]
#                                for c in dict_data[tag][categ]:
#                                    print(c)
                #pp.pprint(final_dict)
                total_list.append(final_dict)
                
        return total_list

weather_dict = dict()
fileList = []
for fileObj in os.walk("."):
    fileList = fileObj[2]
    break
for file in fileList:
# Change SFO to your respective city.
    if "SFO_weather" in file:
        weather_dict[file] = jsonToCSV_weather(file)
fields = []
for date in weather_dict:
    for field in weather_dict[date]:
        fields.append(field)
    break
with open("weather_data.csv", "w") as csvfile:
    writer = csv.DictWriter(csvfile, delimiter = ',', lineterminator = '\n', fieldnames = fields)
    writer.writeheader()
    for date in weather_dict:
        writer.writerow(weather_dict[date])     


yelp_dict = dict()
fileList = []
for fileObj in os.walk("."):
    fileList = fileObj[2]
    break
for file in fileList:
# Change SFO to your respective city.
    if "SFO_Yelp" in file:
        yelp_dict[file] = jsonToCSV_yelp(file)
fields = []
for data in yelp_dict:
    for i in yelp_dict[data]:
        for j in i:
            fields.append(j)
        break
    break
with open("restaurant_data.csv", "w", encoding = "utf8") as csvfile1:
    writer = csv.DictWriter(csvfile1, delimiter = ",", lineterminator = "\n", fieldnames = fields)
    writer.writeheader()
    for data in yelp_dict:
        for i in yelp_dict[data]:
            writer.writerow(i)
