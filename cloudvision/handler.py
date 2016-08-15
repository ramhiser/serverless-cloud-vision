import argparse
import logging
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(here)
sys.path.append(os.path.join(here, "vendored"))

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

from lib import detect_image


def lambda_handler(event, context):
    """AWS Lambda Handler for API Gateway input"""
    image_url = event.get("image_url", "https://raw.githubusercontent.com/ramhiser/serverless-cloud-vision/master/images/ramhiser-and-son.jpg")
    detect_type = event.get("detect_type", "FACE_DETECTION")
    max_results = event.get("max_results", 4)

    logging.debug("Detecting image from URL: %s" % image_url)
    logging.debug("Image detection type: %s" % detect_type)
    logging.debug("Maximum number of results: %s" % max_results)

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

        detection_results = detect_image(args.image_url,
                                         args.detect_type,
                                         args.max_results)

        print detection_results

