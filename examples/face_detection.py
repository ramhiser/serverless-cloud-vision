from PIL import Image
from PIL import ImageDraw
import urllib2
import cStringIO

from lambda_cloudvision import detect_image


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
    if img.headers.maintype != 'image':
        raise TypeError('Invalid filetype given')

    # Source: http://stackoverflow.com/a/7391991/234233
    img_file = cStringIO.StringIO(img.read())
    im = Image.open(img_file)
    img.close()
    draw = ImageDraw.Draw(im)

    for face in faces["responses"][0]["faceAnnotations"]:
        box = [(v.get('x', 0.0), v.get('y', 0.0)) for v in
               face['boundingPoly']['vertices']]
        draw.line(box + [box[0]], width=5, fill='#00ff00')

    del draw
    im.save(output_filename)

if __name__ == '__main__':
    image_url = "https://raw.githubusercontent.com/ramhiser/aws-lambda-cloud-vision/master/images/highlighted-faces.jpg"
    faces = detect_image(image_url, detect_type="FACE_DETECTION")
    highlight_faces(image_url, faces, "images/highlighted-faces.jpg")
