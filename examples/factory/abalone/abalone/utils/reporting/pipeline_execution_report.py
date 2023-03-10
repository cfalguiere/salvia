"""This module contains helper functions to create pipeline's run summaries.

Collects information about the pipeline execution, creates a JSON file, saves the json file,
formats information as a markdown report, and saves the markdown report.
"""
import json
import logging
import os
import traceback
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

import pandas as pd
from jinja2 import Environment, FileSystemLoader
from sagemaker.lineage.visualizer import LineageTableVisualizer

from abalone.utils.reporting.commons import BaseReport, MarkDownContent, ReportContent, JSONDoc, ListOfJSONDocs

# FIXME truncated urls in lineage

pd.set_option("display.max_colwidth", None)


# Type alias
S3LocationURI = str


@dataclass
class PipelineExecutionReportContext:
    """Class for keeping track of report context and data.

    Constructor Arguments
    ---------------------
    sagemaker_session: sagemaker.workflow.pipeline_context.PipelineSession
        The sagemaker session running the pipeline.
    pipeline: sagemaker.workflow.pipeline.Pipeline
        The pipeline instance.
    execution: sagemaker.workflow.pipeline._PipelineExecution
        The pipeline execution instance.
    eval_file_uri: S3LocationURI, optional
        The URL on S3 of the file created by evaluate.
    execution_parameters: dict, optional
        Execution parameters passed as argument to the pipeline start.
    """

    sagemaker_session: Any
    pipeline: Any
    execution: Any
    eval_file_uri: Optional[S3LocationURI] = None
    execution_parameters: Optional[JSONDoc] = None


@dataclass
class PipelineExecutionReportSettings:
    """Class for keeping track of report configuration.

    Constructor Arguments
    ---------------------
    templates_folder: str, defaults to "templates/"
        Directory where the templates could be found.
    markdown_template_filename: str, defaults to "pipeline_execution_report.md"
        Name of file to be used as a template.
    report_folder: str, defaults to "target"
        Name of folder where files created.
    report_filename_radix: str, defaults to "pipeline_execution_report"
        Name of file to be created. .json and .md will be added.
    """

    templates_folder: str = "templates/"
    markdown_template_filename: str = "pipeline_execution_report.md"
    report_folder: str = "target"
    report_filename_radix: str = "pipeline_execution_report"


class PipelineExecutionReport(BaseReport):
    """Class for generating a pipeline execution report."""

    # class variables shared by all instance
    _default_settings = PipelineExecutionReportSettings()

    def __init__(self, settings: PipelineExecutionReportSettings = _default_settings) -> None:
        """Initialize the pipeline execution report.

        Constructor Arguments
        ---------------------
        settings: PipelineExecutionReportSettings
            Configuration of the report. defaults to _default_settings.
        """
        # instance variable unique to each instance
        self.settings = settings

        # initializations
        pass

    def generate_report(self, context: PipelineExecutionReportContext) -> None:
        """Collect pipeline's run information, save a JSON document and a markdown report.

        Parameters
        ----------
        context: PipelineExecutionReportContext
            The context of the execution (sagemaker session, pipeline, execution... .
        """
        logging.info("collecting information for combined report")
        json_report = self.create_combined_json_report(context)
        self.generate_report_from_combined_json(json_report)

    def generate_report_from_combined_json(self, json_report: ReportContent) -> None:
        """Save a JSON document and a markdown report.

        Parameters
        ----------
        json_report: PipelineExecutionContent
            The data collected by create_combined_json_report.
        """
        logging.info("saving JSON and markdown reports")
        os.makedirs(self.settings.report_folder, exist_ok=True)

        json_file_name = f"{self.settings.report_filename_radix}.json"
        json_file_path = os.path.join(self.settings.report_folder, json_file_name)
        self.write_json_report(json_file_path, json_report)

        md_report = self.create_markdown_report(json_report)
        md_file_name = f"{self.settings.report_filename_radix}.md"
        md_file_path = os.path.join(self.settings.report_folder, md_file_name)
        self.write_markdown_report(md_file_path, md_report)

    def create_combined_json_report(self, context: PipelineExecutionReportContext) -> ReportContent:
        """Collect pipeline's run information and creates a JSON document.

        Parameters
        ----------
        context: PipelineExecutionReportContext
            The context of the execution (sagemaker session, pipeline, execution... .

        Returns
        -------
        dict
            The content of the json document consisting in 6 sections
            - "definition",
            - "execution_definition",
            - "execution_steps",
            - "lineage",
            - "execution_parameters",
            - "evaluation"
            An exemple of this document could be found in unit tests.
        """
        definition_report = self._get_pipeline_definition(context.pipeline)

        execution_definition_report = self._get_execution_definition(context.execution)

        execution_steps_report = self._get_execution_steps(context.execution)

        lineage_report = self._get_lineage(context.sagemaker_session, execution_steps_report)

        if context.eval_file_uri:
            evaluation_report = self._get_evaluation(context.sagemaker_session, context.eval_file_uri)
        else:
            evaluation_report = {"error_message": "No evaluation file provided"}

        # combine dicts
        logging.info("building combined report")
        combined_report = {
            "definition": definition_report,
            "execution_definition": execution_definition_report,
            "execution_steps": list(reversed(execution_steps_report)),
            "lineage": lineage_report,
            "execution_parameters": context.execution_parameters,
            "evaluation": evaluation_report,
        }

        # mimic old behavior - parameters were ignored
        if not context.execution_parameters:
            # remove None item
            combined_report.pop("execution_parameters")

        return self._enhance_json(combined_report)

    def create_markdown_report(self, json_report: ReportContent) -> MarkDownContent:
        """Turn the pipeline report's dict into a Markdown document.

        The Markdown document is created from the template located in templates/pipeline_report.md.

        Parameters
        ----------
        json_report: PipelineExecutionContent
            The associative array created by create_combined_json_report.

        Returns
        -------
        str
            a Markdown document.
        """
        logging.info("generating markdown content")
        try:
            environment = Environment(loader=FileSystemLoader(self.settings.templates_folder), autoescape=True)
            template = environment.get_template(self.settings.markdown_template_filename)

            # Avoid to fix all the test data to add an empty element
            if "execution_parameters" in json_report:
                execution_parameters = json_report["execution_parameters"]
            else:
                execution_parameters = {}

            content = template.render(
                definition=json_report["definition"],
                execution_definition=json_report["execution_definition"],
                execution_steps=json_report["execution_steps"],
                evaluation=json_report["evaluation"],
                execution_parameters=execution_parameters,
                lineage=json_report["lineage"],
            )

            return content
        except Exception as err:
            return f"Could not generate report - Reason: {err=}"

    def _fallback_report_data(self, exc: Exception, message: str) -> JSONDoc:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        reason_message = template.format(type(exc).__name__, exc.args)
        stack_trace = traceback.format_exc()
        return {
            "error_message": message,
            "error_reason": reason_message,
            "stack_trace": stack_trace,
        }

    def _get_pipeline_definition(self, pipeline: Any) -> JSONDoc:
        # get pipeline definition as dict
        logging.info("fetching definition")
        try:
            definition_report = JSONDoc(json.loads(pipeline.definition()))
        except (AttributeError, TypeError, ValueError, json.JSONDecodeError) as exc:
            definition_report = self._fallback_report_data(exc, "Could not read pipeline definitions")
        return definition_report

    def _get_execution_definition(self, execution: Any) -> JSONDoc:
        # get the pipeline execution definition as dict
        logging.info("fetching execution definition")
        try:
            execution_definition_report = JSONDoc(execution.describe())
        except (AttributeError, TypeError, ValueError) as exc:
            execution_definition_report = self._fallback_report_data(exc, "Could not read execution definition")
        return execution_definition_report

    def _get_execution_steps(self, execution: Any) -> ListOfJSONDocs:
        # list the steps in the execution as a list of dicts
        logging.info("fetching steps")
        try:
            execution_steps_report = ListOfJSONDocs(execution.list_steps())
        except (AttributeError, TypeError, ValueError) as exc:
            error_status = self._fallback_report_data(exc, "Could not read execution steps")
            execution_steps_report = [error_status]
        return execution_steps_report

    def _get_lineage(
        self, sagemaker_session: Any, execution_steps_report: ListOfJSONDocs
    ) -> ListOfJSONDocs:
        # get the lineage of the artifacts generated by the pipeline as a list of dicts
        logging.info("fetching lineage")
        try:
            viz = LineageTableVisualizer(sagemaker_session.session.Session())
            lineage_report = []
            for execution_step in reversed(ListOfJSONDocs(execution_steps_report)):
                step_name = execution_step["StepName"]
                lineage_df = viz.show(pipeline_execution_step=execution_step)
                if isinstance(lineage_df, pd.DataFrame):
                    step_info = {
                        "stepname": step_name,
                        "items": lineage_df.to_dict(orient="records"),
                    }
                    lineage_report.append(step_info)
        except (AttributeError, TypeError, ValueError) as exc:
            error_status = self._fallback_report_data(exc, "Could not read lineage")
            lineage_report = [error_status]
        return lineage_report

    def _get_evaluation(self, sagemaker_session: Any, eval_file_uri: S3LocationURI) -> JSONDoc:
        # get the model evaluation as dict
        logging.info("fetching evaluation report")
        try:
            evaluation_json = sagemaker_session.s3.S3Downloader.read_file(f"{eval_file_uri}/evaluation.json")
            evaluation_report = JSONDoc(json.loads(evaluation_json))
        except (AttributeError, TypeError, ValueError) as exc:
            evaluation_report = self._fallback_report_data(exc, "Could not read evaluation report")
        return evaluation_report

    def _enhance_json(self, json_report: ReportContent) -> ReportContent:
        dateformat = "%d/%m/%Y %H:%M:%S"

        def enhance_date(step: JSONDoc, key: str) -> None:
            try:
                as_datetime = step[key]
                step[f"{key}AsDatetime"] = as_datetime
                step[f"{key}Short"] = datetime.strftime(as_datetime, dateformat)
            except (ValueError, TypeError):
                step[f"{key}Short"] = "Not Available"  # provide a placeholder for report

        if "error_message" not in json_report["execution_steps"][0]:
            for step in json_report["execution_steps"]:
                enhance_date(step, "StartTime")
                enhance_date(step, "EndTime")

        return json_report
