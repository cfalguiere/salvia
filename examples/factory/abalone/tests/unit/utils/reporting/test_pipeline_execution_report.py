import json
import os
import tempfile
from datetime import datetime

import pytest

# Module under test
from abalone.utils.reporting.pipeline_execution_report import (
    PipelineExecutionReport, PipelineExecutionReportSettings)


@pytest.fixture
def json_path():
    return "tests/unit/utils/reporting/data"


@pytest.fixture
def report_generator():
    return PipelineExecutionReport()


@pytest.fixture
def raw_combined_json_report(json_path):
    filepath = os.path.join(json_path, "report.json")
    try:
        with open(filepath) as json_data:
            combined_json = json.load(json_data)

        # stored data forced data to string. Revert back to data as objects
        for step in combined_json["execution_steps"]:
            start_as_datetime = datetime.fromisoformat(step["StartTime"])
            step["StartTime"] = start_as_datetime
            end_as_datetime = datetime.fromisoformat(step["EndTime"])
            step["EndTime"] = end_as_datetime

        return combined_json
    except FileNotFoundError as exc:
        raise ValueError(f"Could not load data from file {filepath} - reason: {exc}")


@pytest.fixture
def sample_combined_json_report(json_path):
    filepath = os.path.join(json_path, "report.json")
    try:
        with open(filepath) as json_data:
            combined_json = json.load(json_data)

        # mimic the behavior of create_combined_json_report which enhance date before return
        for step in combined_json["execution_steps"]:
            start_as_datetime = datetime.fromisoformat(step["StartTime"])
            step["StartTimeAsDatetime"] = start_as_datetime
            step["StartTimeShort"] = datetime.strftime(
                start_as_datetime, "%d/%m/%Y %H:%M:%S"
            )
            end_as_datetime = datetime.fromisoformat(step["EndTime"])
            step["EndTimeAsDatetime"] = end_as_datetime
            step["EndTimeShort"] = datetime.strftime(
                end_as_datetime, "%d/%m/%Y %H:%M:%S"
            )

        return combined_json
    except FileNotFoundError as exc:
        raise ValueError(f"Could not load data from file {filepath} - reason: {exc}")


@pytest.fixture
def json_report_with_fillers():
    combined_report = {
        "definition": {"error_message": "Could not read pipeline definitions"},
        "execution_definition": {
            "error_message": "Could not read execution definition"
        },
        "execution_steps": [{"error_message": "Could not read execution steps"}],
        "lineage": [{"error_message": "Could not read lineage"}],
        "evaluation": {"error_message": "Could not read evaluation report"},
    }
    return combined_report


@pytest.fixture
def regression_json_report(json_path, report_generator):
    filepath = os.path.join(json_path, "regression_report.json")
    return report_generator.load_json_report(filepath)


@pytest.fixture
def binary_classification_json_report(json_path, report_generator):
    filepath = os.path.join(json_path, "binary_classification_report.json")
    return report_generator.load_json_report(filepath)


@pytest.fixture
def multiclass_json_report(json_path, report_generator):
    filepath = os.path.join(json_path, "multiclass_report.json")
    return report_generator.load_json_report(filepath)


@pytest.fixture
def wrong_date_json_report(json_path):
    filepath = os.path.join(json_path, "wrong_date_report.json")
    try:
        with open(filepath) as json_data:
            combined_json = json.load(json_data)

        # stored data forced data to string. Revert back to data as objects
        # step0 has strings on purpose
        step1 = combined_json["execution_steps"][1]
        start_as_datetime = datetime.fromisoformat(step1["StartTime"])
        step1["StartTime"] = start_as_datetime
        end_as_datetime = datetime.fromisoformat(step1["EndTime"])
        step1["EndTime"] = end_as_datetime

        return combined_json
    except FileNotFoundError as exc:
        raise ValueError(f"Could not load data from file {filepath} - reason: {exc}")


@pytest.fixture
def steps_table_one_step_json_report(json_path, report_generator):
    filepath = os.path.join(json_path, "tables", "steps_table_one_step.json")
    try:
        with open(filepath) as json_data:
            combined_json = json.load(json_data)

        # stored data forced data to string. Revert back to data as objects
        for step in combined_json["execution_steps"]:
            start_as_datetime = datetime.fromisoformat(step["StartTime"])
            step["StartTime"] = start_as_datetime
            end_as_datetime = datetime.fromisoformat(step["EndTime"])
            step["EndTime"] = end_as_datetime

        return report_generator._enhance_json(combined_json)
    except FileNotFoundError as exc:
        raise ValueError(f"Could not load data from file {filepath} - reason: {exc}")


@pytest.fixture
def steps_table_two_steps_json_report(json_path, report_generator):
    filepath = os.path.join(json_path, "tables", "steps_table_two_steps.json")
    try:
        with open(filepath) as json_data:
            combined_json = json.load(json_data)

        # stored data forced data to string. Revert back to data as objects
        for step in combined_json["execution_steps"]:
            start_as_datetime = datetime.fromisoformat(step["StartTime"])
            step["StartTime"] = start_as_datetime
            end_as_datetime = datetime.fromisoformat(step["EndTime"])
            step["EndTime"] = end_as_datetime

        return report_generator._enhance_json(combined_json)
    except FileNotFoundError as exc:
        raise ValueError(f"Could not load data from file {filepath} - reason: {exc}")


@pytest.fixture
def lineage_table_one_line_json_report(json_path, report_generator):
    filepath = os.path.join(json_path, "tables", "lineage_table_one_line.json")
    return report_generator.load_json_report(filepath)


@pytest.fixture
def lineage_table_two_lines_json_report(json_path, report_generator):
    filepath = os.path.join(json_path, "tables", "lineage_table_two_lines.json")
    return report_generator.load_json_report(filepath)


@pytest.fixture
def regression_one_metric_json_report(json_path, report_generator):
    filepath = os.path.join(json_path, "tables", "regression_one_metric_report.json")
    return report_generator.load_json_report(filepath)


# @pytest.mark.xfail
def test_create_combined_json_report(json_report_with_fillers):
    # test robustness
    # should log and provide filler for execution status that it could not fetch
    json_dict = PipelineExecutionReport().create_combined_json_report(
        None, None, None, None
    )

    print(json_dict)

    error_key = "error_message"
    for section_name in [
        "definition",
        "execution_definition",
        "execution_steps",
        "lineage",
        "evaluation",
    ]:
        section = (
            json_dict[section_name][0]
            if section_name in ["execution_steps", "lineage"]
            else json_dict[section_name]
        )
        reference = json_report_with_fillers[section_name]
        expected_error_message = (
            reference[0]["error_message"]
            if section_name in ["execution_steps", "lineage"]
            else reference["error_message"]
        )

        assert "error_message" in section
        assert section["error_message"] == expected_error_message
        assert "error_reason" in section
        assert "An exception of type" in section["error_reason"]
        assert "Arguments" in section["error_reason"]
        assert "stack_trace" in section
        assert "Traceback" in section["stack_trace"]


# @pytest.mark.xfail
def test_create_markdown_report(sample_combined_json_report):
    md_report = PipelineExecutionReport().create_markdown_report(
        sample_combined_json_report
    )

    status_content = "PipelineExecutionStatus: Succeeded"
    assert status_content in md_report


# @pytest.mark.xfail
def test_create_markdown_report_with_fillers(json_report_with_fillers):
    md_report = PipelineExecutionReport().create_markdown_report(
        json_report_with_fillers
    )

    # not included so far
    # assert "Could not read pipeline definitions" in md_report
    assert "Could not read execution definition" in md_report
    assert "Could not read execution steps" in md_report
    assert "Could not read lineage" in md_report
    assert "Could not read evaluation report" in md_report


# @pytest.mark.xfail
def test_enhance_date(raw_combined_json_report):
    enhanced_report = PipelineExecutionReport()._enhance_json(raw_combined_json_report)

    step0 = enhanced_report["execution_steps"][0]

    assert "StartTimeAsDatetime" in step0
    assert isinstance(step0["StartTimeAsDatetime"], datetime)
    assert step0["StartTimeShort"] == "02/12/2022 21:04:09"

    assert "EndTimeAsDatetime" in step0
    assert isinstance(step0["EndTimeAsDatetime"], datetime)
    assert step0["EndTimeShort"] == "02/12/2022 21:08:10"


# @pytest.mark.xfail
def test_enhance_date_wrong_content(wrong_date_json_report):
    enhanced_report = PipelineExecutionReport()._enhance_json(wrong_date_json_report)

    step0 = enhanced_report["execution_steps"][0]

    assert "StartTimeAsDatetime" in step0
    assert step0["StartTimeShort"] == "Not Available"

    assert "EndTimeAsDatetime" in step0
    assert step0["EndTimeShort"] == "Not Available"

    # failure un step 0 should not impact step 1
    step1 = enhanced_report["execution_steps"][1]

    assert "StartTimeAsDatetime" in step1
    assert isinstance(step1["StartTimeAsDatetime"], datetime)
    assert step1["StartTimeShort"] == "02/12/2022 21:10:52"

    assert "EndTimeAsDatetime" in step1
    assert isinstance(step1["EndTimeAsDatetime"], datetime)
    assert step1["EndTimeShort"] == "02/12/2022 21:14:47"


# @pytest.mark.xfail
def test_date_formatting(sample_combined_json_report):
    # shorten date format
    md_report = PipelineExecutionReport().create_markdown_report(
        sample_combined_json_report
    )

    print(md_report)

    step_content = (
        "| AbaloneProcess | 02/12/2022 21:04:09 | 02/12/2022 21:08:10 | Succeeded |"
    )
    assert step_content in md_report


# @pytest.mark.xfail
def test_table_summary_formatting(sample_combined_json_report):
    report_generator = PipelineExecutionReport()
    md_report = report_generator.create_markdown_report(sample_combined_json_report)

    print(md_report)

    execution_definition = sample_combined_json_report["execution_definition"]
    assert execution_definition["PipelineExecutionArn"] in md_report
    assert execution_definition["PipelineExecutionDisplayName"] in md_report
    assert execution_definition["PipelineExecutionStatus"] in md_report
    assert execution_definition["PipelineExecutionDescription"] in md_report
    assert (
        execution_definition["PipelineExperimentConfig"]["ExperimentName"] in md_report
    )
    assert execution_definition["PipelineExperimentConfig"]["TrialName"] in md_report
    assert execution_definition["LastModifiedBy"]["UserProfileName"] in md_report


# @pytest.mark.xfail
def test_table_steps_formatting(
    steps_table_one_step_json_report, steps_table_two_steps_json_report
):
    # ensure table lines are have correct line split and no extra lines
    report_generator = PipelineExecutionReport()
    md_report_1 = report_generator.create_markdown_report(
        steps_table_one_step_json_report
    )
    md_report_2 = report_generator.create_markdown_report(
        steps_table_two_steps_json_report
    )

    print(md_report_1)
    print(md_report_2)

    assert md_report_2.count("\n") == md_report_1.count("\n") + 1

    assert (
        "| AbaloneTrain | 02/12/2022 21:08:23 | 02/12/2022 21:09:45 | Succeeded |"
        in md_report_1
    )


# @pytest.mark.xfail
def test_table_lineage_formatting(
    lineage_table_one_line_json_report, lineage_table_two_lines_json_report
):
    # ensure table lines are have correct line split and no extra lines
    report_generator = PipelineExecutionReport()
    md_report_1 = report_generator.create_markdown_report(
        lineage_table_one_line_json_report
    )
    md_report_2 = report_generator.create_markdown_report(
        lineage_table_two_lines_json_report
    )

    print(md_report_1)
    print(md_report_2)

    assert md_report_2.count("\n") == md_report_1.count("\n") + 1

    l = "| s3://...022-12-02-21-04-06-122/output/validation | Input | DataSet | ContributedTo | artifact |"
    assert l in md_report_1


# @pytest.mark.xfail
def test_table_metrics_formatting(
    regression_one_metric_json_report, regression_json_report
):
    # ensure table lines are have correct line split and no extra lines
    report_generator = PipelineExecutionReport()
    md_report_1 = report_generator.create_markdown_report(
        regression_one_metric_json_report
    )
    md_report_2 = report_generator.create_markdown_report(regression_json_report)

    print(md_report_1)
    print(md_report_2)

    assert md_report_2.count("\n") == md_report_1.count("\n") + 3

    assert "| mae | 0.3711832061068702 | 0.0037566388129940394 |" in md_report_1


@pytest.mark.xfail
def test_long_uri_formatting(sample_combined_json_report):
    # avoid truncated s3 uris
    md_report = PipelineExecutionReport().create_markdown_report(
        sample_combined_json_report
    )

    print(md_report)

    assert "s3://..." not in md_report


# @pytest.mark.xfail
def test_regression_formatting(regression_json_report):
    # sample source: https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-model-quality-metrics.html
    md_report = PipelineExecutionReport().create_markdown_report(regression_json_report)

    print(md_report)

    assert "Report type: regression_metrics" in md_report
    assert "| mse" in md_report
    assert "| rmse" in md_report
    assert "| r2" in md_report


# @pytest.mark.xfail
def test_binary_classification_formatting(binary_classification_json_report):
    # sample source: https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-model-quality-metrics.html
    md_report = PipelineExecutionReport().create_markdown_report(
        binary_classification_json_report
    )

    print(md_report)

    assert "Report type: binary_classification_metrics" in md_report
    assert "Confusion matrix" in md_report
    assert "| no  | 1 | 2 |" in md_report
    assert "| yes | 0 | 1 |" in md_report
    assert "| recall" in md_report
    assert "| precision" in md_report
    assert "| accuracy" in md_report
    assert "| f1" in md_report
    assert "NaN" in md_report


# @pytest.mark.xfail
def test_multiclass_formatting(multiclass_json_report):
    # sample source: https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-model-quality-metrics.html
    md_report = PipelineExecutionReport().create_markdown_report(multiclass_json_report)

    print(md_report)

    assert "Report type: multiclass_classification_metrics" in md_report
    assert "Confusion matrix" in md_report
    assert "| no  | 1180 | 510 |" in md_report
    assert "| yes | 268 | 138 |" in md_report
    assert "| weighted_recall" in md_report
    assert "| weighted_precision" in md_report
    assert "| accuracy" in md_report


# @pytest.mark.xfail
def test_template_not_found(sample_combined_json_report):
    # when template is not found, returns a report with the exception text

    report_settings = PipelineExecutionReportSettings()
    report_settings.markdown_template_filename = "does_not_exist.md"
    md_report = PipelineExecutionReport(
        settings=report_settings
    ).create_markdown_report(multiclass_json_report)
    print(md_report)

    assert (
        "Could not generate report - Reason: err=TemplateNotFound('does_not_exist.md')"
        in md_report
    )


# @pytest.mark.xfail
def test_generate_report_from_combined_json(
    sample_combined_json_report, report_generator
):

    with tempfile.TemporaryDirectory() as tmpdirname:
        report_settings = PipelineExecutionReportSettings()
        report_settings.report_folder = tmpdirname
        md_report = PipelineExecutionReport(
            settings=report_settings
        ).generate_report_from_combined_json(sample_combined_json_report)

        json_filename = os.path.join(tmpdirname, "pipeline_execution_report.json")
        assert os.path.exists(json_filename)

        data = report_generator.load_json_report(json_filename)
        assert data["execution_definition"]["PipelineExecutionStatus"] == "Succeeded"

        md_filename = os.path.join(tmpdirname, "pipeline_execution_report.md")
        assert os.path.exists(md_filename)

        with open(md_filename, "r") as test_file:
            lines = test_file.readlines()
        assert "PipelineExecutionStatus: Succeeded" in lines[8]
