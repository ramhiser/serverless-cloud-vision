# Serverless API around Google Cloud Vision

This project is a serverless API wrapper around
[Google Cloud Vision](https://cloud.google.com/vision/) using
[AWS API Gateway](https://aws.amazon.com/api-gateway/) +
[AWS Lambda](https://aws.amazon.com/lambda/). Deployment is performed with the
[Serverless Framework](http://serverless.com/). The project's API ingests an
image URL and sends the image to Google Cloud Vision for standard image
recognition tasks (e.g., facial detection, OCR, etc.).

## Example Usage

TODO

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

In order to access the Cloud Vision API, you will need to create Google
Application Credentials by following the instructions
[here](https://cloud.google.com/vision/docs/auth-template/cloud-api-auth) for
the **Service Account Key**. Then, download the JSON file with your application
credentials and rename the file as
`cloudvision/google-application-credentials.json`.

After installing Python requirements to the `vendored` folder, we are ready to
deploy our API. At the commandline, type:

```
serverless deploy
```

This command does the following:

* Create IAM roles on AWS for Lambda and API Gateway
* Zips Python code and uploads to S3
* Creates AWS Lambda function
* Creates API Gateway endpoint that triggers AWS Lambda function
