# import pytest

# Module under test
from abalone.pipeline import main


# @pytest.mark.xfail
def test_pipeline():
    rc = main()
    assert rc == 0
