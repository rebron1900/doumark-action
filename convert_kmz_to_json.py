import os
import sys
import json
import zipfile
import xml.etree.ElementTree as ET


def convert_kmz_to_json(kmz_file_path, json_file_path):
    with zipfile.ZipFile(kmz_file_path, 'r') as kmz:
        kml_content = kmz.read('doc.kml')
        
        root = ET.fromstring(kml_content)
        json_content = xml_to_dict(root)
        
        with open(json_file_path, 'w') as json_file:
            json.dump(json_content, json_file, indent=4)
 

def xml_to_dict(element):
    node = {}
    if element.items():
        node.update(dict(element.items()))
    for child in element:
        child_name = child.tag.split('}')[-1]
        child_dict = xml_to_dict(child)
        if child_name in node:
            if isinstance(node[child_name], list):
                node[child_name].append(child_dict)
            else:
                node[child_name] = [node[child_name], child_dict]
        else:
            node[child_name] = child_dict
    if element.text:
        text = element.text.strip()
        if node:
            if text:
                node['text'] = text
        else:
            node = text
    return node


if __name__ == "__main__":
    kmz_file_path = sys.argv[1]
    json_file_path = sys.argv[2]
    convert_kmz_to_json(kmz_file_path, json_file_path)
