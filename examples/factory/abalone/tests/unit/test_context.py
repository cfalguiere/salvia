import os
import tempfile
from pathlib import Path

import pytest

# Module under test
from abalone.context import PipelineContext


# @pytest.mark.xfail
@pytest.mark.pipeline
@pytest.mark.in_container
def test_create_context():

    with tempfile.TemporaryDirectory() as tmpdirname:
        pipeline_context = PipelineContext(
            stage_prefix="X",
            project_prefix="yyy",
            variant_prefix="zzz",
            base_dir=Path("dummy-path"),
            root_folder=tmpdirname,
        )

        print(pipeline_context)

        run_id = pipeline_context.run_id
        assert run_id.isnumeric()
        assert len(run_id) == 10
        assert pipeline_context.job_prefix_short == f"zzz/{run_id}"
        assert pipeline_context.job_prefix_long == f"X/yyy/zzz/{run_id}"
        assert pipeline_context.pipeline_name == "X-yyy-zzz"
        assert pipeline_context.job_name_prefix == "X-yyy-zzz"
        base_folder = pipeline_context.base_folder
        assert base_folder == os.path.join(tmpdirname, f"zzz/{run_id}")
        assert os.path.exists(base_folder)

        # TODO test sagemaker values
