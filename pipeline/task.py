# coding: utf-8

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions


class TemplateOptions(PipelineOptions):

    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_value_provider_argument("--input_csv", type=str)
        parser.add_value_provider_argument("--service_account_file", type=str)
        parser.add_value_provider_argument("--gdrive_directory_id", type=str)


class CopyFile(beam.DoFn):

    def __init__(self, gdrive_directory_id, service_account_file):
        self.gdrive_directory_id = gdrive_directory_id
        self.service_account_file = service_account_file

    def process(self, element):
        import tensorflow as tf
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from apiclient import http
        import csv
        import os
        elements = list(csv.reader([element.encode("utf-8")], delimiter=","))[0]
        gcs_file_path, gdrive_file_name = elements
        # gcs_file_path, gdrive_file_name = element.split(",")
        # gcs_file_path, gdrive_file_name = gcs_file_path.encode("utf-8"), gdrive_file_name.encode("utf-8")
        # Read file in Cloud Storage
        with tf.gfile.Open(gcs_file_path, "rb") as f:
            file_content = f.read()
        # Save file to local disk
        print(gcs_file_path)
        print(gdrive_file_name)
        tf.gfile.MakeDirs("tmp")
        with tf.gfile.Open("tmp/{}".format(gdrive_file_name), "w") as f:
            f.write(file_content)
        # Download service account file
        print(self.service_account_file.get())
        with tf.gfile.Open(self.service_account_file.get(), "rb") as f:
            file_content = f.read()
        with tf.gfile.Open("service_account.json", "w") as f:
            f.write(file_content)
        # Upload file to Google Drive
        scopes = ["https://www.googleapis.com/auth/drive.file"]
        credentials = service_account.Credentials.from_service_account_file(
            "service_account.json",
            scopes=scopes
        )
        service = build("drive", "v3", credentials=credentials, cache_discovery=False)
        media_body = http.MediaFileUpload("tmp/{}".format(gdrive_file_name))
        body = {
            "name": gdrive_file_name,
            "parents": [self.gdrive_directory_id.get()],
        }
        print(body)
        file_ = service.files().create(body=body, fields="id", media_body=media_body).execute()


def main():
    # Create options
    options = PipelineOptions()
    options = options.view_as(beam.options.pipeline_options.SetupOptions)
    options.setup_file = "./setup.py"
    options = options.view_as(beam.options.pipeline_options.GoogleCloudOptions)
    options.job_name = "gcs2gdrive"
    options = options.view_as(TemplateOptions)

    p = beam.Pipeline(options=options)

    (p | "Read" >> beam.io.ReadFromText(options.input_csv)
       | "Write" >> beam.ParDo(CopyFile(options.gdrive_directory_id, options.service_account_file)))

    p.run()


if __name__ == "__main__":
    main()
