from apis.helpers.utils import send_binary_api_requests

url = "https://westus.api.cognitive.microsoft.com/face/v1.0/detect"

image = 'face_api/images/IMG_2630.jpg'

querystring = {"returnFaceId":"true","returnFaceLandmarks":"false","recognitionModel":"recognition_01","returnRecognitionModel":"True","detectionModel":"detection_01"}

send_binary_api_requests(url,querystring,'15262392d8164ba3bb431da6b0c11f42',image)

