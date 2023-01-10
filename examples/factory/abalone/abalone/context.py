"""This module contains information for the pipeline builder."""
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from time import gmtime, strftime
from typing import Any

import sagemaker
from sagemaker.workflow.pipeline_context import PipelineSession


@dataclass
class PipelineContext:
    """Class for keeping track of pipeline context."""

    stage_prefix: str
    project_prefix: str
    variant_prefix: str
    base_dir: Path
    root_folder: str = "./generated"

    sagemaker_session: Any = field(default_factory=sagemaker.session.Session)
    role: Any = field(default_factory=sagemaker.get_execution_role)
    pipeline_session: Any = field(default_factory=PipelineSession)

    def __post_init__(self) -> None:
        logging.info("generating addition context's fields.")
        self.run_id = f"{strftime('%y%m%d%H%M', gmtime())}"
        self.region = self.sagemaker_session.boto_region_name
        self.default_bucket = self.sagemaker_session.default_bucket()
        self.pipeline_name = f"{self.stage_prefix}-{self.project_prefix}-{self.variant_prefix}"
        self.job_prefix_short = f"{self.variant_prefix}/{self.run_id}"
        self.job_prefix_long = f"{self.stage_prefix}/{self.project_prefix}/{self.job_prefix_short}"
        self.job_name_prefix = f"{self.stage_prefix}-{self.project_prefix}-{self.variant_prefix}"
        self.base_uri = f"s3://{self.default_bucket}/{self.job_prefix_long}"
        self.base_uri_for_jobs = f"s3://{self.default_bucket}/{self.stage_prefix}-jobs"
        self.base_folder = os.path.join(self.root_folder, self.job_prefix_short)
        logging.info("creating folders.")
        if not os.path.exists(self.base_folder):
            os.makedirs(self.base_folder)
