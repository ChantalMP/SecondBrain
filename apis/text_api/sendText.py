import json

from apis.helpers.utils import send_json_post_api_requests


url = "https://westus.api.cognitive.microsoft.com/text/analytics/v2.1/keyPhrases"

def get_tags_for_text(text:str):

    payload = "{\n  \"documents\": [\n    {\n      \"language\": \"en\",\n      \"id\": \"1\",\n      \"text\": \"%s\"\n    }\n  ]\n}" % text

    response_text = send_json_post_api_requests(url, {}, 'd77dd9995c9e4714b4a29e6fd124a91d', payload)
    response_text_json = json.loads(response_text)
    key_phrases = response_text_json['documents'][0]['keyPhrases']

    return key_phrases


