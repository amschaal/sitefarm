from link_utils import extract_urls_from_html, check_url
import json, csv

def get_node_links(node):
    try:
        body = node['attributes']['body']['value']
        return extract_urls_from_html(body)
    except:
        print('Node does not have a body')
        return []    
    

def get_all_node_links(filename):
    with open(filename) as f:
        nodes = json.load(f)
        print('{} nodes in file'.format(len(nodes), filename))
        return [{'node': node, 'links': get_node_links(node)} for node in nodes]

def node_links_to_csv(node_links, csv_name, base_url='https://dnatech.genomecenter.ucdavis.edu'):
    with open(csv_name, 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['node_id', 'node_url', 'url', 'is_absolute', 'tag', 'content_type', 'status', 'valid'])
        for nl in node_links:
            node = nl['node']
            for link in nl['links']:
                url = link['url'] if link['is_absolute'] else base_url + link['url']
                print('Checking URL {}'.format(url))
                link_status = check_url(url) or {}
                writer.writerow([node['id'], node['attributes']['path']['alias'],link['url'], link['is_absolute'], link['type'], link_status.get('content_type'), link_status.get('status'), link_status.get('valid')])

def main():
    node_links = get_all_node_links('sf_page.json')
    node_links_to_csv(node_links, 'sf_page_links.tsv')

if __name__ == "__main__":
    main()