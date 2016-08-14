import urllib2
import argparse
import base64
import os

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

API_URL = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'
DETECT_TYPES = ("LABEL_DETECTION", "TEXT_DETECTION", "SAFE_SEARCH_DETECTION",
                "FACE_DETECTION", "LANDMARK_DETECTION", "LOGO_DETECTION",
                "IMAGE_PROPERTIES")

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google-application-credentials.json'


def get_vision_service():
    credentials = GoogleCredentials.get_application_default()
    return discovery.build('vision', 'v1',
                           credentials=credentials,
                           discoveryServiceUrl=API_URL)


def detect_image(image_url, detect_type="FACE_DETECTION", max_results=4):
    """Uses Google Cloud Vision API to detect an entity within an image in the
    given URL.

    Args:
        image_url: a URL containing an image
        detect_type: detection type to perform (default: facial detection)
        max_results: the maximum number of entities to detect within the image
    Returns:
        An array of dicts with information about the entities detected within
        the image.
    """
    if detect_type not in DETECT_TYPES:
        raise TypeError('Invalid detection type given')

    if type(max_results) is not int or max_results <= 0:
        raise TypeError('Maximum results must be a positive integer')

    img = urllib2.urlopen(image_url)
    if img.headers.maintype != 'image':
        raise TypeError('Invalid filetype given')

    batch_request = [{
        'image': {
            'content': base64.b64encode(img.read()).decode('UTF-8')
        },
        'features': [{
            'type': detect_type,
            'maxResults': max_results
        }]
    }]

    img.close()

    service = get_vision_service()
    request = service.images().annotate(
        body={
            'requests': batch_request,
        }
    )
    response = request.execute()
    
    return response


def lambda_handler(event, context):
    """AWS Lambda Handler for API Gateway input"""
    image_url = event["image_url"]
    detect_type = event.get("detect_type", "FACE_DETECTION")
    max_results = event.get("max_results", 4)

    json_return = detect_image(image_url,
                               detect_type,
                               max_results)
    return json_return


if __name__ == '__main__':
        parser = argparse.ArgumentParser(
            description='Detects faces in the given image.'
        )
        parser.add_argument(
            '-i', '--image_url',
            help='The image URL to send to Google Cloud Vision API ',
            required=True
        )
        parser.add_argument(
            '-d', '--detect_type',
            help='detection type to perform. Default: %(default)s',
            default="FACE_DETECTION"
        )
        parser.add_argument(
            '-m', '--max_results',
            help='the max number of entities to detect. Default: %(default)s',
            default=4,
            type=int
        )
        
        args = parser.parse_args()

        from pprint import pprint
        detection_results = detect_image(args.image_url,
                                         args.detect_type,
                                         args.max_results)
        pprint(detection_results)

