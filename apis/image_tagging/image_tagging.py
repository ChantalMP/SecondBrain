import apis.helpers.utils as utils

url = "https://westus.api.cognitive.microsoft.com/vision/v2.0/analyze"
image = 'images/10tipps_kleines_wohnzimmer_home24.jpg'
key = "b601038145984cc789451b5b49b8849d"

#Tags
querystring = {"visualFeatures":"Tags","language":"en"}
utils.send_binary_api_requests(url, querystring, key, image)

#Categories
querystring = {"visualFeatures":"Categories","language":"en"}
utils.send_binary_api_requests(url, querystring, key, image)
