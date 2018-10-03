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

    def __init__(self, gdrive_directory_id):
        self.gdrive_directory_id = gdrive_directory_id

    def process(self, element):
        import tensorflow as tf
        import os
        gcs_file_path, gdrive_file_name = element.split(",")
        # Read file in Cloud Storage
        with tf.gfile.Open(gcs_file_path, "rb") as f:
            file_content = f.read()
        # Save file to local disk
        print(gcs_file_path)
        print(gdrive_file_name)
        tf.gfile.MakeDirs("tmp")
        with tf.gfile.Open("tmp/{}".format(gdrive_file_name), "w") as f:
            f.write(file_content)


def main():
    # Create options
    options = PipelineOptions()
    options = options.view_as(TemplateOptions)

    p = beam.Pipeline(options=options)

    pipeline_input = ["hello", "world"]

    (p | "Read" >> beam.io.ReadFromText(options.input_csv)
       | "Write" >> beam.ParDo(CopyFile(options.gdrive_directory_id)))

    print("hello")
    p.run()


if __name__ == "__main__":
    main()
