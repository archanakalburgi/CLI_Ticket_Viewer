import api_call

def test_get_current_page_num():
    page = api_call.get_current_page_num("invalid uri")
    assert  page == 1

def test_invalid_uri():
    page = api_call.call_zendesk_api("http://invalid-uri.com")
    assert  page == 1 