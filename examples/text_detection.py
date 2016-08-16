import argparse
import json
import requests
from pprint import pprint


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Detects faces in the given image."
    )
    parser.add_argument(
        "-i", "--image_url",
        help="The image URL to send to Google Cloud Vision API ",
        required=True
    )
    parser.add_argument(
        "-m", "--max_results",
        help="the max number of entities to detect. Default: %(default)s",
        default=4,
        type=int
    )
    parser.add_argument(
        "-e", "--endpoint",
        help="The API Gateway endpoint to use",
        required=True
    )

    args = parser.parse_args()

    post_params = {
        "image_url": args.image_url,
        "detect_type": "TEXT_DETECTION",
        "max_results": args.max_results
    }

    # Lazy and used requests in addition to urllib2
    r = requests.post(args.endpoint,
                      data=json.dumps(post_params),
                      headers={'content-type': 'application/json'})
    detection_results = r.json()
    pprint(detection_results)
