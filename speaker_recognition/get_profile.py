import requests

from helpers.utils import send_json_get_api_requests


url = "https://westus.api.cognitive.microsoft.com/spid/v1.0/identificationProfiles"


send_json_get_api_requests(url, {}, '24e9de72f0cc4a27a3d2b4afd43f755f')

