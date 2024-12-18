import csv
import json
import glob
import os
from os.path import join

items_data_file = os.path.join('..','assignment_project_1','collection_items_data.csv')

if os.path.isfile(items_data_file):
    os.unlink(items_data_file)
    print('removed',items_data_file)

row_dict = ()

from datetime import date
date_string_for_today = date.today().strftime('%Y-%m-%d') # see https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
print(date_string_for_today)

list_of_item_metadata_files = list()
for file in glob.glob('C:/Users/madis/Documents/676nlam/assignment_project_1/holiday_item_metadata/holiday_item_metadata-*.json'):
    list_of_item_metadata_files.append(file)

len(list_of_item_metadata_files)     

#Start containers and csv creation script
collection_info_csv = os.path.join('..','assignment_project_1','collection_items_data.csv')
file_count = 0
items_written = 0
error_count = 0

headers = ['item_type', 'date_uploaded', 'source_file', 'creator', 'date', 'digital_id', 'format', 'language', 'location', 'medium', 'subjects', 'title', 'description', 'image_url']

for file in list_of_item_metadata_files:
    file_count += 1
    print('opening',file)
    with open(file, 'r', encoding='utf-8') as item:
        try:
            item_metadata = json.load(item)
        except:
            print('error loading',file)
            error_count += 1
            continue
        item_type = 'Item'
        date_uploaded = date_string_for_today
        source_file = str(file)

        try:
            creator = item_metadata['contributors']
        except:
            creator = 'Not Available'
        try:
            date = item_metadata['date']
        except:
            date = 'Not Available'
        try:
            digital_id = item_metadata['digital_id']
        except:
            digital_id = 'Not Available'
        try:
            format = item_metadata['format'][0]
        except:
            format = 'Not Available'
        try:
            language = item_metadata['language']
        except:
            language = 'Not Available'
        try:
            location = item_metadata['location']
        except:
            location = 'Not Available'
        try:
            medium = item_metadata['medium']
        except:
            medium = 'Not Available'
        try:
            subjects = item_metadata['subjects']
        except:
            subjects = 'Not Available'
        try:
            title = item_metadata['title']
        except:
            title = 'Not Available'
        try:
            description = item_metadata['summary']
        except:
            description = 'Not Available'
        try:
            image_url = item_metadata['image_url'][-1]
        except:
            image_url = 'Not Available'

        row_dict = dict()
        row_dict['item_type'] = item_type
        row_dict['date_uploaded'] = date_uploaded
        row_dict['source_file'] = source_file
        row_dict['creator'] = creator
        row_dict['date'] = date
        row_dict['digital_id'] = digital_id
        row_dict['format'] = format
        row_dict['language'] = language
        row_dict['location'] = location
        row_dict['medium'] = medium
        row_dict['subjects'] = subjects
        row_dict['title'] = title
        row_dict['description'] = description
        row_dict['image_url'] = image_url
        print('created row dictionary:', row_dict)

        with open(collection_info_csv, 'a', encoding='utf-8') as fout:
            writer = csv.DictWriter(fout, fieldnames=headers)
            if items_written == 0:
                writer.writeheader()
            writer.writerow(row_dict)
            items_written += 1
            print('adding',digital_id)

print('\n\n--- LOG ---')
print('wrote',collection_info_csv)
print('with',items_written,'items')
print(error_count,'errors (info not written)')