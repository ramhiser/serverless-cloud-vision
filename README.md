# Serverless API around Google Cloud Vision

This project is a serverless API wrapper around
[Google Cloud Vision](https://cloud.google.com/vision/) using
[AWS API Gateway](https://aws.amazon.com/api-gateway/) +
[AWS Lambda](https://aws.amazon.com/lambda/). Deployment is performed with the
[Serverless Framework](http://serverless.com/).

## Usage

The API Gateway endpoint accepts an image URL and triggers a Lambda function,
which ingests the image from a URL and sends the image to Google Cloud Vision
for standard image recognition tasks (e.g., facial detection, OCR, etc.).

For instance, the following `curl` command sends an image URL to the API Gateway.

```
curl -H "Content-Type: application/json" -X POST \
-d '{"image_url": "https://raw.githubusercontent.com/ramhiser/serverless-cloud-vision/master/examples/images/ramhiser-and-son.jpg"}' \
https://some-api-gateway.execute-api.us-east-1.amazonaws.com/dev/detect_image
```

The response JSON includes a variety of metadata to describe the faces detected:

```
{
  "responses": [
    {
      "faceAnnotations": [
        {
          "angerLikelihood": "VERY_UNLIKELY",
          "blurredLikelihood": "VERY_UNLIKELY",
          "boundingPoly": {
            "vertices": [
              {
                "x": 512,
                "y": 249
              },
              {
                "x": 637,
                "y": 249
              },
              {
                "x": 637,
                "y": 395
              },
              {
                "x": 512,
                "y": 395
              }
            ]
          },
          "detectionConfidence": 0.98645973,
          ...
```

In the `examples` folder, we provide a script that produces a new image with
bounding boxes around the faces detected:

![highlighted faces](https://raw.githubusercontent.com/ramhiser/serverless-cloud-vision/master/examples/images/highlighted-faces.jpg)

Beyond facial detection, Google Cloud Vision [supports the following image
recognition tasks](https://cloud.google.com/vision/docs/requests-and-responses):

* `LABEL_DETECTION`
* `TEXT_DETECTION`
* `SAFE_SEARCH_DETECTION`
* `FACE_DETECTION`
* `LANDMARK_DETECTION`
* `LOGO_DETECTION`
* `IMAGE_PROPERTIES`

## Google Cloud Vision Credentials

In order to access the Cloud Vision API, you will need to create Google
Application Credentials by following the instructions
[here](https://cloud.google.com/vision/docs/common/auth#set_up_a_service_account) for
the **Service Account Key**. Then, download the JSON file with your application
credentials and rename the file as
`cloudvision/google-application-credentials.json`.

## Deployment

Make sure you have Node.js 4.0+ installed. Then, install the [Serverless Framework](https://github.com/serverless/serverless).

```
npm install serverless -g
```

Install any Python dependencies to the `cloudvision/vendored` folder.

```
pip install -t cloudvision/vendored/ -r requirements.txt
```

**NOTE**: Homebrew + Mac OS users who encounter the `DistutilsOptionError` error
should see [this SO post](http://stackoverflow.com/a/24357384/234233) for a fix.

After installing Python requirements to the `vendored` folder, type the
following at the commandline to deploy the wrapper API:

```
serverless deploy
```

This command does the following:

* Create IAM roles on AWS for Lambda and API Gateway
* Zips Python code and uploads to S3
* Creates AWS Lambda function
* Creates API Gateway endpoint that triggers AWS Lambda function

## Examples

Example Python scripts are available in the `examples` folder. These examples
require that the API (described above) be successfully deployed. As [mentioned by
Chris Cooper](https://github.com/ramhiser/serverless-cloud-vision/issues/3), the
Python dependencies must be installed locally in order to run the examples. To
do this, type the following locally:

```
pip install -r requirements.txt
```
