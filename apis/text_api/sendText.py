from apis.helpers.utils import send_json_post_api_requests

url = "https://westus.api.cognitive.microsoft.com/text/analytics/v2.1/keyPhrases"

payload = "{\n  \"documents\": [\n    {\n      \"language\": \"en\",\n      \"id\": \"1\",\n      \"text\": \"How does my dog look like?\"\n    }\n  ]\n}"

send_json_post_api_requests(url, {}, 'd77dd9995c9e4714b4a29e6fd124a91d', payload)

