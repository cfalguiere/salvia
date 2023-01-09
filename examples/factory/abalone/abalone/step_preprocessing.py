"""This module implements a SageMaker pipeline's step for preprocessing data."""

import logging
from typing import Any, Optional

from sagemaker.processing import ProcessingInput, ProcessingOutput, RunArgs
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.workflow.parameters import ParameterInteger, ParameterString

from abalone.context import PipelineContext
from abalone.utils.reporting.pipeline_execution_report import PipelineExecutionReport, PipelineExecutionReportContext


def create_preprocessing_run_args(
    context: PipelineContext,
    instance_type_param: ParameterString,
    processing_instance_count_param: ParameterInteger,
    input_data_param: ParameterString,
) -> Optional[RunArgs]:
    """Create the step definition for a preprocessing step."""
    logging.info("setting up the preprocessing step")

    framework_version = "0.23-1"

    sklearn_processor = SKLearnProcessor(
        framework_version=framework_version,
        instance_type=instance_type_param,
        instance_count=processing_instance_count_param,
        base_job_name=f"{context.job_name_prefix}-preprocess",
        role=context.role,
        sagemaker_session=context.pipeline_session,
    )

    processor_run_args = sklearn_processor.run(
        inputs=[
            ProcessingInput(source=input_data_param, destination="/opt/ml/processing/input"),
        ],
        outputs=[
            ProcessingOutput(output_name="train", source="/opt/ml/processing/train"),
            ProcessingOutput(output_name="validation", source="/opt/ml/processing/validation"),
            ProcessingOutput(output_name="test", source="/opt/ml/processing/test"),
        ],
        code=(context.base_dir / "pipeline_scripts/preprocessing.py").as_uri(),
    )
    # TODO path to pipeline_scripts as parameter -> script_dir
    # TODO constante for path /opt/ml/processing

    return processor_run_args
