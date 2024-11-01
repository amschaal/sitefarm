import http.client
import json
import base64
import urllib

site = json.load(open('.siteinfo.json'))

categories = json.load(open('faq_categories.json'))
cat_dict = {}
for c in categories['data']:
    cat_dict[c['attributes']['name']] = {
                                "type": "taxonomy_term--faq",
                                "id": c['id'],
                                "meta": {
                                    "drupal_internal__target_id": c['attributes']['drupal_internal__tid']
                                }
                            }

wp_faqs = json.load(open('wordpress_export.json'))

def create_node(wp_faq):
    print(wp_faq)
    parsed = urllib.parse.urlparse(wp_faq['link'])
    path = parsed.path
    categories = [ cat_dict[cat] for cat in wp_faq['categories'] if cat in cat_dict ]
    if len(categories) == 0:
        categories = ["01 General Information"]
    node_data = {
        "data": 
            {
                "type": "node--faq",
                "attributes": {
                    "title": wp_faq['title'],
                    "body": {
                        "value": wp_faq['content'],
                        "format": "basic_html"
                    },
                    "path": {
                        "alias": path,
                        "langcode": "en",
                        "pathauto": False
                    }
                },
                "relationships": {
                    "field_faq_category": {
                        "data": categories
                    }
                }
            }
    }
    return node_data


def create_drupal_node(drupal_url, username, password, node_data):
    headers = {
        'Content-Type': 'application/vnd.api+json',
        'Accept': 'Accept: application/vnd.api+json',
        'Authorization': 'Basic ' + base64.b64encode(f"{username}:{password}".encode()).decode()
    }
    # Create a connection
    conn = http.client.HTTPSConnection(drupal_url)

    try:
        # Send a POST request
        conn.request("POST", 'https://'+drupal_url + "/jsonapi/node/faqs", json.dumps(node_data), headers)
        
        # Get the response
        response = conn.getresponse()
        data = response.read()

        # Print the response
        print(f"Status: {response.status}, Reason: {response.reason}")
        print("Response:", data.decode())
    finally:
        conn.close()

def main():
    for faq in wp_faqs:
        node_data = create_node(faq)
        print(faq)
        print('-------')
        print (node_data)
        print('************')
        create_drupal_node(site['site'], site['username'], site['password'], node_data)

if __name__ == "__main__":
    main()