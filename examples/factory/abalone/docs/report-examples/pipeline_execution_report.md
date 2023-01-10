

# Execution

## Summary

| Name      | Value |
| --------- | ----- |
| PipelineExecutionArn | arn:aws:sagemaker:eu-west-1:999999999999:pipeline/f-abalone-xgb/execution/cos5h1n0dv8j |
| PipelineExecutionDisplayName | execution-1672925433971 |
| PipelineExecutionStatus | Failed |
| PipelineExecutionDescription |  |
| ExperimentName | f-abalone-xgb |
| TrialName | cos5h1n0dv8j |
| UserProfileName | lili |
| FailureReason | Step failure: One or multiple steps failed. |

## Parameters

| Name      | Type | DefaultValue | Value |
| --------- | ---- | ------------ | ----- |
| ProcessingInstanceCount | Integer | 1 |  |
| TrainingInstanceType | String | ml.m5.large |  |
| InputData | String | s3://sagemaker-eu-west-1-999999999999/L/abalone/xgbjob/2301031407/abalone-dataset.csv | s3://sagemaker-eu-west-1-999999999999/L/abalone/xgbjob/2301031407/abalone-dataset.csv |


## Steps

| Name      | StartTime | EndTime | StepStatus | Reason |
| --------- | --------- | ------- | ---------- | ------ |
| PreProcess | 05/01/2023 13:30:35 | 05/01/2023 13:30:36 | Failed | ClientError: Failed to invoke sagemaker:CreateProcessingJob. Error Details: The account-level service limit &#39;ml.m5.large for processing job usage&#39; is 0 Instances, with current utilization of 0 Instances and a request delta of 1 Instances. Please contact AWS support to request an increase for this limit. Retry not appropriate on execution of step with PipelineExecutionArn arn:aws:sagemaker:eu-west-1:999999999999:pipeline/f-abalone-xgb/execution/cos5h1n0dv8j and StepId PreProcess. No retry policy configured for the exception type SAGEMAKER_RESOURCE_LIMIT. |


## Lineage



## Evaluation


Data not available:
No evaluation file provided

