import argparse
import json
import urllib2
import requests
import cStringIO

from PIL import Image
from PIL import ImageDraw


def highlight_faces(image_url, faces, output_filename):
    """Draws a polygon around the faces, then saves to output_filename.

    Args:
      image_url: a URL containing an image
      faces: a list of faces found in the file. This should be in the format
          returned by the Vision API.
      output_filename: the name of the image file to be created, where the
          faces have polygons drawn around them.
    """
    img = urllib2.urlopen(image_url)
    if img.headers.maintype != "image":
        raise TypeError("Invalid filetype given")

    # Source: http://stackoverflow.com/a/7391991/234233
    img_file = cStringIO.StringIO(img.read())
    im = Image.open(img_file)
    img.close()
    draw = ImageDraw.Draw(im)

    for face in faces["responses"][0]["faceAnnotations"]:
        box = [(v.get("x", 0.0), v.get("y", 0.0)) for v in
               face["boundingPoly"]["vertices"]]
        draw.line(box + [box[0]], width=5, fill="#00ff00")

    del draw
    im.save(output_filename)


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
    parser.add_argument(
        "-o", "--output",
        help="The filename of the output image. Default: %(default)s",
        default="images/highlighted-faces.jpg"
    )

    args = parser.parse_args()

    post_params = {
        "image_url": args.image_url,
        "detect_type": "FACE_DETECTION",
        "max_results": args.max_results
    }

    # Lazy and used requests in addition to urllib2
    r = requests.post(args.endpoint,
                      data=json.dumps(post_params),
                      headers={'content-type': 'application/json'})
    detection_results = r.json()

    highlight_faces(args.image_url, detection_results, args.output)
