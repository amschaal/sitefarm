from download_api_data import get_all_data
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
    

def get_all_node_links(api_url):
    nodes = get_all_data(api_url)
    return [{'node': node, 'links': get_node_links(node)} for node in nodes]

def node_links_to_csv(node_links, csv_name, domain):
    url_checker = URLChecker()
    with open(csv_name, 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['node_id', 'node_url', 'url', 'link text', 'is_absolute', 'tag', 'content_type', 'status', 'valid'])
        for nl in node_links:
            node = nl['node']
            for link in nl['links']:
                url = link['url'] if link['is_absolute'] else 'https://' + domain + link['url']
                # if to_domain:
                #     url = translate_url(url, from_domain=from_domain, to_domain=to_domain)
                print('Checking URL {}'.format(url))
                try:
                    page_url = 'https://'+domain+node['attributes']['path']['alias']
                except:
                    page_url = 'Page URL unspecified'
                try:
                    link_status = url_checker.check_url(url) or {}
                    writer.writerow([node['id'], page_url, url, (link.get('text') or 'N/A')[:30], link['is_absolute'], link['type'], link_status.get('content_type'), link_status.get('status'), link_status.get('valid')])
                except Exception as e:
                    print('Failed to check link {}.  Exception: {}'.format(url, str(e)))
                    writer.writerow([node['id'], page_url, url, (link.get('text') or 'N/A')[:30], None, None, None, 'Error', None])
                
    # url_checker.close_connections()
def main():
    content_type = 'sf_page'
    site = json.load(open('.siteinfo.json'))
    api_url = 'https://{}/jsonapi/node/{}'.format(site['site'], content_type)
    node_links = get_all_node_links(api_url)
    node_links_to_csv(node_links, '{}_links.tsv'.format(content_type), domain=site['site'])

if __name__ == "__main__":
    main()