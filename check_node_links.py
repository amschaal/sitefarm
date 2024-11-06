from link_utils import URLChecker, extract_urls_from_html, translate_url
import json, csv

def get_node_html(node):
    try:
        return node['attributes']['body']['value']
    except:
        return None

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

def node_links_to_csv(node_links, csv_name, from_domain, to_domain=None):
    url_checker = URLChecker()
    with open(csv_name, 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['node_id', 'node_url', 'url', 'is_absolute', 'tag', 'content_type', 'status', 'valid'])
        for nl in node_links:
            node = nl['node']
            for link in nl['links']:
                url = link['url'] if link['is_absolute'] else 'https://' + from_domain + link['url']
                if to_domain:
                    url = translate_url(url, from_domain=from_domain, to_domain=to_domain)
                print('Checking URL {}'.format(url))
                link_status = url_checker.check_url(url) or {}
                writer.writerow([node['id'], node['attributes']['path']['alias'], url, link['is_absolute'], link['type'], link_status.get('content_type'), link_status.get('status'), link_status.get('valid')])
    # url_checker.close_connections()
def main():
    node_links = get_all_node_links('sf_page.json')
    node_links_to_csv(node_links, 'sf_page_link_translated_test.tsv', from_domain='dnatech.genomecenter.ucdavis.edu', to_domain='dnatech.sf.ucdavis.edu')

if __name__ == "__main__":
    main()