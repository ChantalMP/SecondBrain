from apis.helpers.utils import send_json_post_api_requests

url = "https://westus.api.cognitive.microsoft.com/face/v1.0/verify"

face_id_1 = 'bc23ce53-af29-45c9-98f3-776b81dc4aab'
face_id_2 = 'f59d0332-4dea-482e-a1f6-e1681f234a7e'

payload = ("{\n    \"faceId1\": \"%s\",\n    \"faceId2\": \"%s\"\n}" % (face_id_1,face_id_2))


send_json_post_api_requests(url, {}, '15262392d8164ba3bb431da6b0c11f42', payload)
