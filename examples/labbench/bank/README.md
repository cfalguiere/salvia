# Salvia Banks Example for LabBench stage

This section consists in experiments and notebooks examples based on the banks dataset used on AWS labs.

# Dataset 

These examples are based on the bank dataset

https://archive.ics.uci.edu/ml/datasets/bank+marketing


# Problem solving 

Based on this tutorial on Bank with autotuning

https://sagemaker-examples.readthedocs.io/en/latest/hyperparameter_tuning/xgboost_random_log/hpo_xgboost_random_log.html
Old tutorial https://docs.aws.amazon.com/en_jp/sagemaker/latest/dg/automatic-model-tuning-ex-data.html


Solutions for this classification problem as in notebooks
- Make use of SageMaker Autopilot/AutoML with / without some data preparation
- Make use of the SageMaker Autotuning job

Use Studio's prebuilt image DataScience 3.0 (conda) and XGBoost Stack

# Reference

Documentation about bank and autotuning

- https://docs.aws.amazon.com/en_jp/sagemaker/latest/dg/automatic-model-tuning-ex-data.html
- https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning.html
- https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-ex.html


Documentation about the AutoML feature

- https://sagemaker.readthedocs.io/en/stable/api/training/automl.html
- https://dataintegration.info/launch-amazon-sagemaker-autopilot-experiments-directly-from-within-amazon-sagemaker-pipelines-to-easily-automate-mlops-workflows
- https://docs.aws.amazon.com/sagemaker/latest/dg/build-and-manage-steps.html
- https://aws.amazon.com/blogs/machine-learning/move-amazon-sagemaker-autopilot-ml-models-from-experimentation-to-production-using-amazon-sagemaker-pipelines/
- https://sagemaker-examples.readthedocs.io/en/latest/autopilot/autopilot_customer_churn_high_level_with_evaluation.html
- https://sagemaker-examples.readthedocs.io/en/latest/sagemaker-pipelines/tabular/automl-step/sagemaker_autopilot_pipelines_native_auto_ml_step.html


API documentation
- https://sagemaker-examples.readthedocs.io/en/latest/hyperparameter_tuning/xgboost_random_log/hpo_xgboost_random_log.html
- https://fig.io/manual/aws/sagemaker/create-hyper-parameter-tuning-job
- https://docs.aws.amazon.com/sagemaker/latest/dg/automatic-model-tuning-monitor.html
- https://sagemaker.readthedocs.io/en/stable/api/training/automl.html
