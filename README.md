# dataflow-gcs2gdrive

This is an implementation of Dataflow Template copying files from Google Cloud Storage to Google Drive.

## Input Parameters for Dataflow Template

### query

A query string whose result is a table below:

| gcs_file_path      | gdrive_file_name    |
|:------------------:|:-------------------:|
| gs://gcs/file/path | file_name_in_gdrive |
| ...                | ...                 |

### service_account_file

Google Cloud Storage path of the service account file, for example `gs://your-bucket/hoge.json`.
This service account is used to access Google Drive API.

### gdrive_directory_id

The ID of the destination directory in Google Drive.
The files in Google Cloud Storage will be copied to this directory.

Note that the service account should have permission to access this directory.

TODO: image

## Deploy Dataflow Template

```bash
PROJECT_ID="<Your Project ID>"

python -m pipeline.task \
  --runner DataflowRunner \
  --project ${PROJECT_ID} \
  --staging_location gs://${PROJECT_ID}-dataflow/staging \
  --temp_location gs://${PROJECT_ID}-dataflow/temp \
  --template_location gs://${PROJECT_ID}-dataflow/templates/gcs2gdrive
```

## Use Dataflow Template

TODO
