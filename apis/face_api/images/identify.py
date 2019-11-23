from apis.helpers.utils import send_json_post_api_requests, send_binary_api_requests
import json
from apis.face_api.detect import get_person_id

url = "https://westus.api.cognitive.microsoft.com/face/v1.0/verify"

person_group_id = 'persondatabase'

key = '15262392d8164ba3bb431da6b0c11f42'

def identify():
    url = "https://westus.api.cognitive.microsoft.com/face/v1.0/identify"
    person_id = get_person_id("apis/face_api/images/talle_test.jpg")
    querystring = {}
    body = r'{"personGroupId":"persondatabase", "faceIds":["' + person_id + r'"], "maxNumOfCandidatesReturned":1}'
    code, text = send_json_post_api_requests(url, querystring, key, body)
    print(code)
    print(text)

def create_peson(name):
    url = "https://westus.api.cognitive.microsoft.com/face/v1.0/persongroups/{}/persons".format(person_group_id)
    querystring = {}
    body = "{\"name\":\"" + name + "\"}"
    _, text = send_json_post_api_requests(url, querystring, key, body)
    return json.loads(text)['personId']

def add_image_to_person(person_id, image):
    url = "https://westus.api.cognitive.microsoft.com/face/v1.0/persongroups/persondatabase/persons/{}/persistedFaces".format(person_id)
    querystring = {}
    header, text = send_binary_api_requests(url, querystring, key, image)
    print(header)
    print(text)



#create_peson("Marcel") 203418ce-26cd-4769-bff0-43afdf675370
#create_peson("Ege") 588ca96a-8493-47c5-8b28-d656ec63cc9b
#create_peson("Michi") c03ee496-f4cf-4985-ad06-d46a7ec27467
#create_peson("Chantal") 8186f04a-dba0-4dd9-86ca-32f961b17631

#add_image_to_person("588ca96a-8493-47c5-8b28-d656ec63cc9b", "apis/face_api/images/ege2.jpg")

#identify()