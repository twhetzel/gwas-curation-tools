# GWAS Curation Tools

## Description
This script finds mentions of ancestry terms from the [Human Ancestry Ontology](https://www.ebi.ac.uk/ols/ontologies/hancestro) in PDF files. The file processing features of this script were based on the Google Cloud tutorial to [process images asynchronously](https://cloud.google.com/run/docs/tutorials/image-processing) using Cloud Run.


## Dependencies
PDF Miner
Python
Flask
Google Cloud Buid
Google Container Registry
Google Pub/Sub
Google Cloud Storage
Google Cloud Run
Google Cloud SDK


## Usage
* Analyze a PDF file as:
`gsutil cp ~/PATH-TO-PDF-FILE/pmid_31196165.pdf gs://gwas-pdf && gsutil cp gs://gwas-results/results-pmid_31196165.txt LOCAL-RESULTS-DIRECTORY/`


## Set-up
* Install dependencies as:
`pip install requirements.txt`

* Install Google Cloud SDK
See [Google Cloud SDK documentation](https://cloud.google.com/sdk/docs) for installation details for your operating system.

* Set-up gcloud defaults
  1. Set your default project:
  `gcloud config set project PROJECT-ID`

  2. Configure gcloud for your chosen region:
  `gcloud config set run/region REGION`

* Set-up Cloud Storage buckets
  1. Create Cloud Storage bucket for input file, where INPUT_BUCKET_NAME is a globally unique bucket name:
  `gsutil mb gs://INPUT_BUCKET_NAME`

  2. Create a second Cloud Storage bucket to receive the result file, where BLURRED_BUCKET_NAME is a globally unique bucket name:
  `gsutil mb gs://BLURRED_BUCKET_NAME`

* Ship the code
Shipping the code includes three steps: building a container image with Cloud Build, uploading the container image to Container Registry, and deploying the container image to Cloud Run.

  1. Build your container and publish on Container Registry:
  `gcloud builds submit --tag gcr.io/PROJECT_ID/pubsub`

  2. Deploy the service:
  `gcloud run deploy pubsub-tutorial --image gcr.io/PROJECT_ID/pubsub --set-env-vars=BLURRED_BUCKET_NAME=BLURRED_BUCKET_NAME`

* Turn on notifications from Cloud Storage
Configure Cloud Storage to publish a message to a Pub/Sub topic whenever a file (known as an object), is uploaded or changed. Send the notification to the previously created topic so any new file upload will invoke the service.
`gsutil notification create -t myRunTopic -f json gs://INPUT_BUCKET_NAME`


