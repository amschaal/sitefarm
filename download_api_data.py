"""
A simple script for quickly downloading all of the drupal nodes from an API endpoint (results are limited to 50 nodes).
It writes out the results to a JSON file for further scripting.
"""

import json
from urllib.request import urlopen


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

def save_api_data(filename, site_url, path=None, node_type='sf_article'):
    if not path:
        path = '/jsonapi/node/{}'.format(node_type)
    url = 'https://{}{}'.format(site_url, path)
    data = get_all_data(url)
    print('{} nodes downloaded for API call: {}'.format(len(data), url))
    json.dump(data, open(filename,'w'), indent=4)
