"""
A simple script for quickly downloading all of the drupal nodes from an API endpoint (results are limited to 50 nodes).
It writes out the results to a JSON file for further scripting.
"""

import json
from urllib.request import urlopen
site = json.load(open('.siteinfo.json'))

def get_json(url):
    with urlopen(url) as resource:
        return json.load(resource)

def get_all_data(api_url):
    print("Get all data for URL: {}".format(api_url))
    all_data = []
    url = api_url
    while url:
        print("Fetch {}".format(url))
        data = get_json(url)
        all_data += data['data']
        url = data.get('links', {}).get('next', {}).get('href', None)
    return all_data

site = site['site']
node_type = 'sf_article' # sf_page
url = 'https://{}/jsonapi/node/{}'.format(site, node_type)
filename = '{}.json'.format(node_type)
data = get_all_data(url)
print('{} nodes downloaded for node type: {}'.format(len(data), node_type))
json.dump(data, open(filename,'w'), indent=4)