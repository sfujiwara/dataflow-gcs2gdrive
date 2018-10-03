# dataflow-gcs2gdrive

This is an implementation of Dataflow Template copying files from Google Cloud Storage to Google Drive.

## Input Parameters for Dataflow Template

### input_csv

A Google Cloud Storage path of input CSV file, for example `gs://hoge/fuga.csv`.

The CSV has two columns:

- Google Cloud Storage File Path
- Google Drive File Name

| gcs_file_path      | gdrive_file_name    |
|:------------------:|:-------------------:|
| gs://gcs/file/path | file_name_in_gdrive |
| ...                | ...                 |

Note that the CSV should not have header row as below:

```csv
gs://gcs/file/path1,file_name_in_gdrive1
gs://gcs/file/path2,file_name_in_gdrive2
...
```

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
pip install -r requirements.txt
```

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
