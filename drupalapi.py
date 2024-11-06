import http.client
import json
import base64

site = json.load(open('.siteinfo.json'))

def get_connection(drupal_url, username, password):
    headers = {
        'Content-Type': 'application/vnd.api+json',
        'Accept': 'Accept: application/vnd.api+json',
        'Authorization': 'Basic ' + base64.b64encode(f"{username}:{password}".encode()).decode()
    }

    # Create a connection
    conn = http.client.HTTPSConnection(drupal_url)
    return headers, conn

def create_drupal_node(drupal_url, username, password, path, node_data, verbose=False):

    headers, conn = get_connection(drupal_url, username, password)

    try:
        # Send a POST request
        conn.request("POST", 'https://'+drupal_url + path, json.dumps(node_data), headers)
        
        # Get the response
        response = conn.getresponse()
        data = response.read()

        if verbose:
            # Print the response
            print(f"Status: {response.status}, Reason: {response.reason}")
            print("Response:", data.decode())
    finally:
        conn.close()

    return response

def update_drupal_node(drupal_url, username, password, path, node_data, verbose=False):
    
    headers, conn = get_connection(drupal_url, username, password)

    try:
        # Send a POST request
        conn.request("PATCH", 'https://'+drupal_url + path, json.dumps(node_data), headers)
        
        # Get the response
        response = conn.getresponse()
        data = response.read()

        if verbose:
            # Print the response
            print(f"Status: {response.status}, Reason: {response.reason}")
            print("Response:", data.decode())
    finally:
        conn.close()

    return response

def main():
    # Just for testing
    drupal_url = site['site']
    username = site['username']
    password = site['password']

    # Node data to create
    node_data = { #example
        "data": 
            {
                "type": "node--faq",
                "attributes": {
                    "title": "API Test FAQ",
                    "body": {
                        "value": "Testing API...",
                        "format": "basic_html"
                    },
                },
                "relationships": {
                    "field_faq_category": {
                        "data": [
                            {
                                "type": "taxonomy_term--faq",
                                "id": "da33f148-f3a4-4403-aa0e-70cf12de843c",
                                "meta": {
                                    "drupal_internal__target_id": 91
                                }
                            }
                        ]
                    }
                }
            }
    }

    create_drupal_node(drupal_url, username, password, node_data)

if __name__ == "__main__":
    main()