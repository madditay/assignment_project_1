import requests
import json
import csv
endpoint = 'https://www.loc.gov/free-to-use'
parameters = {
    'fo' : 'json'
}
collection = 'holidays'
collection_r = requests.get(endpoint + '/' + collection, params=parameters)
collection_r.url
print('You requested:',collection_r.url)
print('HTTP server response code:',collection_r.status_code)

collection_json = collection_r.json()
print('Data Elements:', collection_json.keys())

for key in collection_json['content']['set']['items']:
    print(key)
    
print('Total number of items:', len(collection_json['content']['set']['items']))

collection_set = '../assignment_project_1/holiday_set.csv'
headers = ['image', 'link', 'title']

with open(collection_set, 'w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for item in collection_json['content']['set']['items']:
        item['title'] = item['title'].rstrip()
        writer.writerow(item)
    print('Data has been written to', collection_set)


