import pytest
import src.util


def test_invalid_uri():
    pytest.raises(Exception, src.util.get_current_page_num, "invalid uri")
