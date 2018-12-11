# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 18:12:05 2018

@author: AkshayJk
"""

import csv
import pandas as pd

def rest_review_change():
    review_dict = dict()
    with open("rest_data_combined.csv", "r", encoding = 'utf8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        prev_val = 0
        for row in reader:
            if row[3] not in review_dict:
                review_dict[row[3]] = []
                prev_val = int(row[6])
                review_dict[row[3]].append(0)
            else:
                ans = int(row[6]) - prev_val
                prev_val = int(row[6])
                review_dict[row[3]].append(ans)
    print(review_dict['&pizza'])

rest_review_change()