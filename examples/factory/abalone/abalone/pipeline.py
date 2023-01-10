"""This module implements a SageMaker pipeline."""

import logging
import os
import sys
from pathlib import Path

import boto3
import sagemaker
from sagemaker.workflow.parameters import ParameterInteger, ParameterString
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep

from abalone.context import PipelineContext
from abalone.step_preprocessing import create_preprocessing_run_args
from abalone.utils.reporting.pipeline_execution_report import PipelineExecutionReport, PipelineExecutionReportContext

# INIT

# logging initialisations


BASE_DIR = Path(__file__).parent


def main() -> int:
    """Create and run the pipeline."""
    buildpath = "build"
    if not os.path.exists(buildpath):
        os.makedirs(buildpath)

    root_logger = logging.getLogger()
    # root_logger.setLevel(logging.DEBUG) # or whatever
    root_logger.setLevel(logging.INFO)  # or whatever
    handler = logging.FileHandler(f"{buildpath}/pipeline-definition.log", "w", "utf-8")
    formatter = logging.Formatter("%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    # sagemaker initialisations
    logging.info("setting the pipeline context.")

    context = PipelineContext(
        stage_prefix="F",
        project_prefix="abalone",
        variant_prefix="xgb",
        base_dir=BASE_DIR,
    )

    logging.info(f"context is {context}.")

    # code_dir = os.path.join(BASE_DIR, 'pipeline_scripts')

    # execution parameters
    logging.info("setting parameters.")

    processing_instance_count_param = ParameterInteger(name="ProcessingInstanceCount", default_value=1)
    instance_type_param = ParameterString(name="TrainingInstanceType", default_value="ml.m5.large")  # "ml.m5.xlarge"

    # Datasets
    logging.info("loading datasets.")

    logging.info(f"base_folder is {context.base_folder}.")
    datapath = os.path.join(context.base_folder, "data")
    if not os.path.exists(datapath):
        os.makedirs(datapath)

    local_path = os.path.join(datapath, "abalone-dataset.csv")

    s3 = boto3.resource("s3")
    # s3.Bucket("sagemaker-sample-files").download_file("datasets/tabular/uci_abalone/abalone.csv", local_path)
    s3.Bucket(f"sagemaker-servicecatalog-seedcode-{context.region}").download_file(
        "dataset/abalone-dataset.csv", local_path
    )
    input_data_uri = sagemaker.s3.S3Uploader.upload(local_path=local_path, desired_s3_uri=context.base_uri)
    logging.info(input_data_uri)

    input_data_param = ParameterString(
        name="InputData",
        default_value="s3://sagemaker-eu-west-1-102959664345/L/abalone/xgbjob/2301031407/abalone-dataset.csv",
    )

    # STEP AbaloneProcess (preprocessor)
    logging.info("creating preprocessing step.")

    preprocessing_run_args = create_preprocessing_run_args(
        context, instance_type_param, processing_instance_count_param, input_data_param
    )
    step_process = ProcessingStep(name="PreProcess", step_args=preprocessing_run_args)

    # preprocessor_outputs = step_process.properties.ProcessingOutputConfig.Outputs

    # PIPELINE definition

    logging.info("gathering the pipeline steps.")

    pipeline = Pipeline(
        name=context.pipeline_name,
        parameters=[
            processing_instance_count_param,
            instance_type_param,
            input_data_param,
        ],
        steps=[step_process],
    )

    # submit the pipeline

    logging.info("updating the pipeline.")
    pipeline.upsert(role_arn=context.role)

    # RUN

    logging.info("configuring and starting the pipeline.")
    execution_parameters = dict(
        InputData="s3://sagemaker-eu-west-1-102959664345/L/abalone/xgbjob/2301031407/abalone-dataset.csv"
        # ModelApprovalStatus="Approved",
        # MseThreshold=3.0
    )

    execution = pipeline.start(
        parameters=execution_parameters,
        # execution_display_name=eid,
        # execution_description="DEV with defaults",
    )

    logging.info("waiting for the pipeline to end.")

    error = 0
    try:
        execution.wait()
    except Exception as exc:
        error = 1
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(exc).__name__, exc.args)
        logging.error(message)
        logging.exception(exc)
        # pdb.post_mortem()

    # REPORT

    logging.info("producing reports.")

    report_context = PipelineExecutionReportContext(
        sagemaker_session=context.pipeline_session,
        pipeline=pipeline,
        execution=execution,
        execution_parameters=execution_parameters,
    )

    report_generator = PipelineExecutionReport()
    report_generator.generate_report(context=report_context)

    return error


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
