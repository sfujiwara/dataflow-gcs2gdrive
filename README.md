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
This service account is only used to access Google Drive API.

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

```python
from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials

project_id = 'your-gcp-project-id'
input_csv = 'gs://your/input/csv/file.csv'
gdrive_directory_id = 'your-output-gdrive-directory-id'
service_account_file = 'gs://your/service/account/file.json'
dataflow_template = "gs://{}-dataflow/templates/gcs2gdrive".format(project_id)

credentials = GoogleCredentials.get_application_default()
service = build("dataflow", "v1b3", credentials=credentials, cache_discovery=False)
body = {
    "jobName": "hoge-gcs2gdrive-fuga",
    "parameters": {
        "input_csv": input_csv,
        "gdrive_directory_id": gdrive_directory_id,
        "service_account_file": service_account_file
    },
    "environment": {
        "tempLocation": "gs://{}-dataflow/temp".format(project_id),
        "zone": "us-central1-f"
    }
}
request = service.projects().templates().launch(
    projectId=project_id,
    gcsPath=dataflow_template,
    body=body,
)
response = request.execute()
```

## Frequently Asked Questions

### How can we deal with file name or GCS Path which contains `,`?

Quote with `"` as below:

```
gs://gcs/file/path,"google,drive,file,name.pdf"
```

### We want to use `/` for a file name on Google Drive

Sorry, we does not support it...
Please replace with other strings.