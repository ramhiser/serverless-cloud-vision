import logging
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(here)

from lib import detect_image


def lambda_handler(event, context):
    """AWS Lambda Handler for API Gateway input"""
    post_args = event.get("body", {})
    image_url = post_args["image_url"]
    detect_type = post_args.get("detect_type", "FACE_DETECTION")
    max_results = post_args.get("max_results", 4)

    logging.debug("Detecting image from URL: %s" % image_url)
    logging.debug("Image detection type: %s" % detect_type)
    logging.debug("Maximum number of results: %s" % max_results)

    json_return = detect_image(image_url,
                               detect_type,
                               max_results)
    return json_return


