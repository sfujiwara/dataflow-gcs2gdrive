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

    def __init__(self, gcs_file_path):
        self.gcs_file_path = gcs_file_path

    def process(self, element):
        import tensorflow as tf
        import os
        gcs_path = os.path.join(self.gcs_dir.get(), element)
        with tf.gfile.Open(gcs_path, "w") as f:
            f.write("test")


def main():
    # Create options
    options = PipelineOptions()
    options = options.view_as(TemplateOptions)

    p = beam.Pipeline(options=options)

    pipeline_input = ["hello", "world"]

    (p | "Read" >> beam.Create(pipeline_input)
       | "Write" >> beam.ParDo(CopyFile(options.gcs_file_path)))

    p.run()


