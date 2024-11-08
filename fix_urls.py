from download_api_data import get_all_data
from drupalapi import update_drupal_node
from check_node_links import get_node_html, get_node_links
from link_utils import replace_urls_in_attributes, translate_url
import json
site = json.load(open('.siteinfo.json'))


def update_node_html(node, html):
    node_data = {
           'data': {
               'type': node['type'],
               'id': node['id'],
               'attributes': {
                    'body': {
                        'value': html,
                        'format': 'basic_html'
                    }
               }
           }
       }
    return update_drupal_node(site['site'], site['username'], site['password'], '/jsonapi/node/faqs/{}'.format(node['id']), node_data)
    

def update_urls(list_nodes_api_url, commit=False, limit=10):
    nodes = get_all_data(list_nodes_api_url)
    same = []
    diff = []
    for node in nodes[:limit+1]:
        html = get_node_html(node)
        if html:
            new_html = replace_urls_in_attributes(html, site['old_site'])
            # new_html = new_html.replace('http://', 'https://').replace(site['old_site'], site['site'])
            if html == new_html:
                same.append(node['id'])
                print("---Skipping https://{}{}".format(site['site'], node['attributes']['path']['alias']))
            else:
                diff.append(node['id'])
                print("+++Updating https://{}{}".format(site['site'], node['attributes']['path']['alias']))
                if commit:
                    update_node_html(node, new_html)
    print("Same: {}".format(len(same)))
    print("Updated: {}".format(len(diff)))
    print("Updated: "+', '.join(diff))

# update_urls('https://{}/jsonapi/node/sf_article'.format(site['site']), commit=False, limit=100)
# update_urls('https://{}/jsonapi/node/sf_page'.format(site['site']), commit=False, limit=1000)
update_urls('https://{}/jsonapi/node/faqs'.format(site['site']), commit=False, limit=100)