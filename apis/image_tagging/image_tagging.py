import json

import apis.helpers.utils as utils

url = "https://westus.api.cognitive.microsoft.com/vision/v2.0/analyze"
key = "b601038145984cc789451b5b49b8849d"


def get_tags_for_image(image_path):
    # Tags
    querystring = {"visualFeatures": "Tags", "language": "en"}
    _, raw_data = utils.send_binary_api_requests(url, querystring, key, image_path)
    raw_data_json = json.loads(raw_data)
    tags = [elem['name'] for elem in raw_data_json['tags']]

    # Categories
    querystring = {"visualFeatures": "Categories", "language": "en"}
    _, raw_data = utils.send_binary_api_requests(url, querystring, key, image_path)
    raw_data_json = json.loads(raw_data)
    categories = [elem['name'] for elem in raw_data_json['categories']]


    return tags + categories