{# templates/report.md #}

# Execution

## Summary

{% if "error_message" not in execution_definition  -%}
| Name      | Value | 
| --------- | ----- | 
| PipelineExecutionArn | {{ execution_definition['PipelineExecutionArn'] }} |
| PipelineExecutionDisplayName | {{ execution_definition['PipelineExecutionDisplayName'] }} |
| PipelineExecutionStatus | {{ execution_definition['PipelineExecutionStatus'] }} |
| PipelineExecutionDescription | {{ execution_definition['PipelineExecutionDescription'] }} |
| ExperimentName | {{ execution_definition['PipelineExperimentConfig']['ExperimentName'] }} |
| TrialName | {{ execution_definition['PipelineExperimentConfig']['TrialName'] }} |
| UserProfileName | {{ execution_definition['LastModifiedBy']['UserProfileName'] }} |
{% if "FailureReason" in execution_definition  -%}
| FailureReason | {{ execution_definition['FailureReason'] }} |
{%- endif  %}
{%- else  %}
Data not available:
{{ execution_definition['error_message'] }}
{{ execution_definition['error_reason'] }}
{{ execution_definition['stack_trace'] }}
{%- endif  %}

## Parameters

| Name      | Type | DefaultValue | Value | 
| --------- | ---- | ------------ | ----- | 
{% for parameter in definition["Parameters"] -%}
{% set name = parameter['Name'] -%}
{% if name in execution_parameters -%}
| {{parameter['Name']}} | {{parameter['Type']}} | {{parameter['DefaultValue']}} | {{execution_parameters[name]}} |
{%- else -%}
| {{parameter['Name']}} | {{parameter['Type']}} | {{parameter['DefaultValue']}} |  |
{%- endif  %}
{% endfor %}

## Steps

{% if "error_message" not in execution_steps[0]  -%}
| Name      | StartTime | EndTime | StepStatus | Reason |
| --------- | --------- | ------- | ---------- | ------ |
{% for step in execution_steps -%}
{% set has_error = 'FailureReason' in step -%}
{% set reason = step['FailureReason'] if has_error else "" -%}
| {{step['StepName']}} | {{step['StartTimeShort']}} | {{step['EndTimeShort']}} | {{step['StepStatus']}} | {{reason | replace("\n", " ")}} |
{% endfor %}
{%- else  %}
Data not available:
{{ execution_steps[0]['error_message'] }}
{% if "error_reason" in execution_steps[0]  -%}
{{ execution_steps[0]['error_reason'] }}
{%- endif  %}
{% if "stack_trace" in execution_steps[0]  -%}
{{ execution_steps[0]['stack_trace'] }}
{%- endif  %}
{%- endif  %}

## Lineage

{% if "error_message" not in lineage[0]  -%}
{% for step in lineage -%}

### {{step['stepname']}}

| Name/Source   | Direction | Type | Association Type | Lineage Type |
| ------------- | --------- | ---- | ---------------- | ------------ |
{% for item in step['items']  -%}
| {{item['Name/Source']}} | {{item['Direction']}} | {{item['Type']}} | {{item['Association Type']}} | {{item['Lineage Type']}} |
{% endfor  %}
{% endfor -%}
{%- else  %}
Data not available:
{{ lineage[0]['error_message'] }}
{{ lineage[0]['error_reason'] }}
{{ lineage[0]['stack_trace'] }}
{%- endif  %}

## Evaluation

{% if "error_message" not in evaluation  -%}
{% for evaluation_key, evaluation_value in evaluation.items() -%}
Report type: {{ evaluation_key }}
{% if "confusion_matrix" in evaluation_value -%}
{% set confusion_matrix = evaluation_value["confusion_matrix"] -%}
Confusion matrix
|     | no | yes |
| no  | {{confusion_matrix['0']['0']}} | {{confusion_matrix['0']['1']}} |
| yes | {{confusion_matrix['1']['0']}} | {{confusion_matrix['1']['1']}} |
{% endif %}

| Metric   | Value | Standard Deviation |
| -------- | ----- | ------------------ |
{% for metric_key, metric_value in evaluation_value.items() -%}
{% if 'value' in metric_value -%}
| {{metric_key}} | {{metric_value['value']}} | {{metric_value['standard_deviation']}} |
{%- endif %}
{% endfor  %}
{%- endfor  %}
{%- else  %}
Data not available:
{{ evaluation['error_message'] }}
{{ evaluation['error_reason'] }}
{{ evaluation['stack_trace'] }}
{%- endif  %}
