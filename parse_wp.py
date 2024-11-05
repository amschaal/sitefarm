import xml.etree.ElementTree as ET
import json

def parse_wp_xml(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Initialize a list to hold posts
    posts = []

    # Namespace for WordPress XML format
    namespace = {
                    'wp': 'http://wordpress.org/export/1.2/',
                    'content': 'http://purl.org/rss/1.0/modules/content/'
                }

    # Iterate over each item in the XML
    for item in root.findall('.//item'):
        try:
            # content = item.find('content:encoded', namespace)
            # print(content.text)
            post = {}
            post['title'] = item.find('title').text
            post['link'] = item.find('link').text
            post['post_name'] =  item.find('wp:post_name', namespace).text
            post['content'] = item.find('content:encoded', namespace).text

            # Get additional metadata (e.g., categories, tags)
            categories = [category.text for category in item.findall('category')]
            post['categories'] = categories

            posts.append(post)
        except Exception as e:
            print('bad', item)
            print(e)

    return posts

def export_to_json(data, json_file):
    # Export the parsed data to a JSON file
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    xml_file = 'wordpress_export.xml'  # Replace with your XML file path
    json_file = 'wordpress_export.json'  # Desired output JSON file path

    # Parse the XML file
    posts = parse_wp_xml(xml_file)

    # Export to JSON
    export_to_json(posts, json_file)

    print(f"Exported {len(posts)} posts to {json_file}")

if __name__ == "__main__":
    main()