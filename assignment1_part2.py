import csv
import json
import requests
import os
from os.path import join

def regenerate_collection_list(collection_csv):
    collection_items = list()
    with open(collection_csv, 'r', encoding='utf-8', newline='') as file:
        data = csv.DictReader(file)
        for row in data:
            row_dict = dict()
            for field in data.fieldnames:
                row_dict[field] = row[field]
            collection_items.append(row_dict)
        return collection_items

collection_csv = os.path.join('..','assignment_project_1','collection_set.csv')
collection_set_list = regenerate_collection_list(collection_csv)
collection_set_list[0]

baseURL = 'https://www.loc.gov'
parametrs = {'fo': 'json'}

item_metadata_directory = os.path.join('..','assignment_project_1','item_metadata')

if os.path.isdir(item_metadata_directory):
    print(item_metadata_directory, 'exists')
else:
    os.mkdir(item_metadata_directory)
    print('created', item_metadata_directory)

item_count = 0
error_count = 0
file_count = 0

data_directory = 'assignment_project_1'
item_metadata_directory = 'item_metadata'
item_metadata_file_prefix = 'item_metadata'
json_suffix = '.json'

for item in collection_set_list:
    if item['link'] == 'link':
        continue
    if '?' in item['link']:
        resource_ID = item['link']
        short_ID = item['link'].split('/')[2]
        item_metadata = requests.get(baseURL + resource_ID, params={'fo':'json'})
        print('requested',item_metadata.url,item_metadata.status_code)
        if item_metadata.status_code != 200:
            print('requested',item_metadata.url,item_metadata.status_code)
            error_count += 1
            continue
        try:
            item_metadata.json()
        except: #basically this catches all of the highsmith photos with hhh in the ID
            error_count += 1
            print('no json found')
            continue
        fout = os.path.join('..',data_directory, item_metadata_directory, str(item_metadata_file_prefix + '-' + short_ID + json_suffix))
        with open(fout, 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(item_metadata.json()['item']))
            file_count += 1
            print('wrote', fout)
        item_count += 1
    else:
        resource_ID = item['link']
        short_ID = item['link'].split('/')[2]
        item_metadata = requests.get(baseURL + resource_ID, params={'fo':'json'})
        print('requested',item_metadata.url,item_metadata.status_code)
        if item_metadata.status_code != 200:
            print('requested',item_metadata.url,item_metadata.status_code)
            error_count += 1
            continue
        try:
            item_metadata.json()
        except:
            error_count += 1
            print('no json found')
            continue
        fout = os.path.join('..',data_directory, item_metadata_directory, str(item_metadata_file_prefix + '-' + short_ID + json_suffix))
        with open(fout, 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(item_metadata.json()['item']))
            file_count += 1
            print('wrote', fout)
        item_count += 1

print('--- mini log ---')
print('items processed:', item_count)
print('errors:', error_count)
print('files created:', file_count)

main_dir = os.path.join('C:\\', 'Users', 'madis', 'Documents', '676nlam')
project_dir = 'assignment_project_1'
files_dir = 'item-files'
metadata_dir = 'item_metadata'

files_location = os.path.join(main_dir, project_dir, files_dir)
print('Checking for...', files_location)

if os.path.isdir(files_location):
    print("Files directory already exists")
else:
    os.makedirs(files_location)
    print("Files directory created", files_location)

import glob

search_for_metadata_here = os.path.join('..',project_dir,metadata_dir)
print('Searching for metadata here...')
metadata_file_list = glob.glob(search_for_metadata_here + '/*.json')
print('Found:', metadata_file_list)

item_image_urls = list()
count = 0

for item in metadata_file_list:
    with open(item, 'r', encoding='utf-8') as file:
        metadata = json.load(file)
        image_url_no = len(metadata['image_url'])
        image_url = metadata['image_url'][-1]
        item_image_urls.append(image_url)
        count += 1

print(f'Identified { str(count) } image URLs')

item_image_urls

collection_set_list_with_images = list()

for item in metadata_file_list:
    with open(item, 'r', encoding='utf-8') as item_info:
        item_metadata = json.load(item_info)

        # add the metadata into a dictionary for each item
        item_metadata_dict = dict()
        item_metadata_dict['item_URI'] = item_metadata['id']
        try:
            item_metadata_dict['lccn'] = item_metadata['library_of_congress_control_number']
        except:
            item_metadata_dict['lccn'] = None
        item_metadata_dict['title'] = item_metadata['title']
        item_metadata_dict['image_URL_large'] = item_metadata['image_url'][-1]
        
        # add the metadata to the main list
        collection_set_list_with_images.append(item_metadata_dict)

print(collection_set_list_with_images[0])

item_count = 0
error_count = 0
file_count = 0

img_file_prefix = 'img_'

for item in collection_set_list_with_images:
    image_URL = item['image_URL_large']
    short_ID = item['item_URI'].split('/')[-2]
    print('... requesting', image_URL)
    item_count += 1

    # if found, save image
    r = requests.get(image_URL)
    if r.status_code == 200:
        img_out = os.path.join(files_location, str(img_file_prefix + short_ID + '.jpg'))
        with open(img_out, 'wb') as file:
            file.write(r.content)
            print('Saved', img_out)
            file_count += 1
    else:
        error_count += 1

print('--- mini LOG ---')
print('files requested:',item_count)
print('errors:',error_count)
print('files written:',file_count)