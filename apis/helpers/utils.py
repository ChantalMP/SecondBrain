import requests

from typing import Dict

def send_binary_api_requests(url:str, querystring:Dict[str,str], subscribtion_key:str, data_url:str):


    headers = {
        'Ocp-Apim-Subscription-Key': '{}'.format(subscribtion_key),
        'Content-Type': "application/octet-stream",
    }

    data = open('{}'.format(data_url), 'rb').read()

    response = requests.post(url=url,
                             data=data,
                             headers=headers, params=querystring)

    return dict(response.headers),response.text


def send_json_post_api_requests(url:str, querystring:Dict[str, str], subscribtion_key:str, payload:str):


    headers = {
        'Ocp-Apim-Subscription-Key': '{}'.format(subscribtion_key),
        'Content-Type': "application/json",
    }


    response = requests.post(url=url,
                             data=payload,
                             headers=headers, params=querystring)

    return response.status_code, response.text

def send_json_post_api_train():


    headers = {
        'Ocp-Apim-Subscription-Key': '{}'.format("15262392d8164ba3bb431da6b0c11f42"),
    }

    url = "https://westus.api.cognitive.microsoft.com/face/v1.0/persongroups/persondatabase/train"
    response = requests.post(url=url,
                             data={},
                             headers=headers, params={})

    return response.status_code, response.text

def send_json_get_api_requests(url:str, querystring:Dict[str, str], subscribtion_key:str):


    headers = {
        'Ocp-Apim-Subscription-Key': '{}'.format(subscribtion_key),
        'Content-Type': "application/json",
    }


    response = requests.get(url=url,
                             headers=headers, params=querystring)


    return response.status_code, response.text

