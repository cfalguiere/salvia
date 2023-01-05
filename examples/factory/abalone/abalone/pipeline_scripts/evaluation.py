"""This module contains the evaluation script used by the pipeline."""

import json
import os
import pathlib
import pickle  # noqa
import tarfile

import numpy as np
import pandas as pd
import xgboost
from sklearn.metrics import mean_squared_error


def evaluation(base_dir):
    """Do the model evaluation.

    Data are passed by the step's channels (Input and Output).
    The model and the inout file are copied onto /opt/ml/processing/test
    by the processor and input channel.
    The evaluation file written onto /opt/ml/processing/evaluation
    will be made available on S3 by the Output Channel.

    Parameters
    ----------
    base_dir: str
        The root folder for exchanges with the step or unit test.
    """
    model_path = os.path.join(base_dir, "model", "model.tar.gz")
    with tarfile.open(model_path) as tar:
        tar.extractall(path=".")

    model = pickle.load(open("xgboost-model", "rb"))  # noqa

    test_path = os.path.join(base_dir, "test", "test.csv")
    df = pd.read_csv(test_path, header=None)

    y_test = df.iloc[:, 0].to_numpy()
    df.drop(df.columns[0], axis=1, inplace=True)

    X_test = xgboost.DMatrix(df.values)

    predictions = model.predict(X_test)

    mse = mean_squared_error(y_test, predictions)
    std = np.std(y_test - predictions)
    report_dict = {
        "regression_metrics": {
            "mse": {"value": mse, "standard_deviation": std},
        },
    }

    output_dir = os.path.join(base_dir, "evaluation")
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    evaluation_path = f"{output_dir}/evaluation.json"
    with open(evaluation_path, "w") as f:
        f.write(json.dumps(report_dict))


if __name__ == "__main__":
    """Do the model evaluation. This is intended to be run is a SageMaker Processor."""

    base_dir = "/opt/ml/processing"
    evaluation(base_dir)
    # TODO test errors
    # sys.exit(1)
