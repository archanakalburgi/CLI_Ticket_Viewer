import pytest
import util


def test_invalid_uri():
    pytest.raises(Exception, util.get_current_page_num, "invalid uri")
