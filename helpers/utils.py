import requests

from typing import Dict

def send_binary_api_requests(url:str,querystring:Dict[str,str],subscribtion_key:str,img_url:str):


    headers = {
        'Ocp-Apim-Subscription-Key': '{}'.format(subscribtion_key),
        'Content-Type': "application/octet-stream",
    }

    data = open('{}'.format(img_url), 'rb').read()

    response = requests.post(url=url,
                             data=data,
                             headers=headers, params=querystring)

    print(response.text)


def send_json_api_requests(url:str,querystring:Dict[str,str],subscribtion_key:str,payload:str):


    headers = {
        'Ocp-Apim-Subscription-Key': '{}'.format(subscribtion_key),
        'Content-Type': "application/json",
    }


    response = requests.post(url=url,
                             data=payload,
                             headers=headers, params=querystring)

    print(response.text)
