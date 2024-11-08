import re
from html import unescape
import http.client
import urllib.parse

def extract_urls_from_html(html_string):
    # Regular expression patterns for extracting URLs
    img_pattern = r'<img [^>]*src="([^"]*)"[^>]*>'
    a_pattern = r'<a [^>]*href="([^"]*)"[^>]*>(.*?)</a>'
    # Pattern to find absolute URLs not in tags
    text_url_pattern = r'(?<!["\'>])https?://[^\s<]+(?!["\'>])'

    urls = []

    # Find all img tags
    for match in re.findall(img_pattern, html_string):
        url = match
        is_absolute = bool(urllib.parse.urlparse(url).scheme)
        urls.append({
            'url': match,
            'type': 'img',
            'text': None,  # No text associated with img tags,
            'is_absolute': is_absolute,
            'found_in': 'tag'
        })

    # Find all anchor tags
    for match in re.findall(a_pattern, html_string):
        url, text = match
        is_absolute = bool(urllib.parse.urlparse(url).scheme)
        urls.append({
            'url': url,
            'type': 'a',
            'text': unescape(text.strip()),  # Unescape HTML entities
            'is_absolute': is_absolute,
            'found_in': 'tag'
        })
    
    # Find all absolute URLs in the text that are not part of HTML tags
    for match in re.findall(text_url_pattern, html_string):
        if bool(urllib.parse.urlparse(match).scheme):  # Ensure it's an absolute URL
            urls.append({
                'url': match,
                'type': None,
                'text': None,
                'is_absolute': True,
                'found_in': 'text'
            })

    return [url for url in urls if (url['url'].lower().startswith("http://") or url['url'].lower().startswith("https://") or url['url'].startswith("/"))]

def replace_urls_in_attributes(html, domain):
    # Regular expression to match HTML tag attributes that contain URLs (href, src, etc.)
    tag_url_pattern = r'(\b(?:href|src|action|data)\s*=\s*["\'])((https?://[^\s\'"]+))(["\'])'
    
    # Normalize the input domain to lowercase
    domain = domain.lower()

    def replace_url(match):
        # Get the full URL from the match
        url = match.group(2)
        parsed_url = urllib.parse.urlparse(url)
        
        # Check if the domain matches the given domain
        if parsed_url.netloc.lower() == domain:
            # Rebuild the URL with only the path, query, and fragment (if present)
            new_url = urllib.parse.urlunparse((
                '', '', parsed_url.path, '', parsed_url.query, parsed_url.fragment
            ))
            # Return the updated attribute with the new URL path
            return match.group(1) + new_url + '"'
        else:
            # If the domain doesn't match, return the original tag with the unchanged URL
            return match.group(0)
    
    # Use re.sub to replace URLs within attributes in the HTML
    return re.sub(tag_url_pattern, replace_url, html)

def translate_url(url, from_domain, to_domain):
    url = url.replace('http://', 'https://').replace(from_domain, to_domain)
    return url

class URLChecker:
    def __init__(self) -> None:
        self.checked_urls = {}
        # self.connections = {}
    # def close_connections(self):
    #     for key in self.connections.keys():
    #         conn = self.connections.pop(key)
    #         conn.close()
    # def get_connection(self, netloc):
    #     if netloc not in self.connections:
    #         # Parse the URL into components
    #         # Create a connection based on the scheme (http or https)
    #         # if parsed_url.scheme == 'https':
    #         self.connections[netloc] =  http.client.HTTPSConnection(netloc, timeout=10)
    #         # else:
    #             # self.connections[url] =  http.client.HTTPConnection(parsed_url.netloc, timeout=10)
    #     return self.connections[netloc]
    def check_url(self, url):
        if url in self.checked_urls:
            return self.checked_urls[url]
        parsed_url = urllib.parse.urlparse(url)
        link = {'url': url}
        if parsed_url.scheme == 'https':
            conn = http.client.HTTPSConnection(parsed_url.netloc, timeout=10)
        else:
            conn = http.client.HTTPConnection(parsed_url.netloc, timeout=10)
        try:
            # Make a HEAD request to minimize data transfer
            conn.request("HEAD", parsed_url.path or "/")  # Use "/" if path is empty
            response = conn.getresponse()

            # Get content type from the headers
            link['content_type'] = response.getheader('Content-Type')
            link['status'] = response.status

            # Check status codes
            if response.status == 200:
                link['valid'] = True
            else:
                link['valid'] = False
            self.checked_urls[url] = link
        except Exception as e:
            print('Exception', url, e)
            return False
        finally:
            conn.close()
        
        return link

def main():
    html_string = '''
        <html>
            <body>
                <a href="http://example.com">Example</a>
                <img src="http://example.com/image.png" alt="Image">
                <a href="https://another-example.com">Another Example</a>
                <a href="/relative/link">Another Example</a>
                http://ucdavis.edu
                and
                https://ucdavis.edu/foobazle
            </body>
        </html>
    '''

    links = extract_urls_from_html(html_string)
    print(links)
    print('statuses:')
    for link in links:
        print(check_url(link['url']))

if __name__ == "__main__":
    main()
