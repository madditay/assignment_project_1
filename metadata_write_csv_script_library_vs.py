import csv
import json
import glob
import os
from os.path import join

items_data_file = os.path.join('..','assignment_project_1','library_items_data.csv')

if os.path.isfile(items_data_file):
    os.unlink(items_data_file)
    print('removed',items_data_file)

row_dict = ()

from datetime import date
date_string_for_today = date.today().strftime('%Y-%m-%d') # see https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
print(date_string_for_today)

list_of_item_metadata_files = list()
for file in glob.glob('C:/Users/madis/Documents/676nlam/assignment_project_1/item_metadata/item_metadata-*.json'):
    list_of_item_metadata_files.append(file)

len(list_of_item_metadata_files)     

#Start containers and csv creation script
collection_info_csv = os.path.join('..','assignment_project_1','library_items_data.csv')
file_count = 0
items_written = 0
error_count = 0

headers = ['item_type', 'date_uploaded', 'source_file', 'item_id', 'title', 'date', 'source_url', 'phys_format', 'dig_format', 'rights', 'image_url']

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
            item_id = item_metadata['library_of_congress_control_number']
        except:
            item_id = item_metadata['url'].split('/')[-2]
        title = item_metadata['title']
        try:
            date = item_metadata['date']
        except:
            date = 'Not found'
        source_url = item_metadata['url']
        try:
            phys_format = item_metadata['format'][0]
        except:
            phys_format = 'Not found'
        try:
            dig_format = item_metadata['online_format'][0]
        except:
            dig_format = 'Not found'
        mime_type = item_metadata['mime_type']
        try:
            rights = item_metadata['rights_information']
        except:
            rights = 'Undetermined'
        try:
            image_url = item_metadata['image_url'][-1]
            #[len(item_metadata['item']['image_url']) - 1]
        except:
            image_url = 'Did not identify a URL.'

        row_dict = dict()
        row_dict['item_type'] = item_type
        row_dict['date_uploaded'] = date_uploaded
        row_dict['source_file'] = source_file
        row_dict['item_id'] = item_id
        row_dict['title'] = title
        row_dict['date'] = date
        row_dict['source_url'] = source_url
        row_dict['phys_format'] = phys_format
        row_dict['dig_format'] = dig_format.capitalize()
        row_dict['rights'] = rights
        row_dict['image_url'] = image_url
        print('created row dictionary:', row_dict)

        with open(collection_info_csv, 'a', encoding='utf-8') as fout:
            writer = csv.DictWriter(fout, fieldnames=headers)
            if items_written == 0:
                writer.writeheader()
            writer.writerow(row_dict)
            items_written += 1
            print('adding',item_id)

print('\n\n--- LOG ---')
print('wrote',collection_info_csv)
print('with',items_written,'items')
print(error_count,'errors (info not written)')