import api
import pytest
import responses
from requests.exceptions import HTTPError
import json


def test_invalid_uri():
    pytest.raises(Exception, api.get_current_page_num, "invalid uri")


@responses.activate
def test_404_should_not_kill_2():
    responses.add(
        responses.GET, "https://zccarchanazendeskcom.zendesk.com/", status=500
    )
    pytest.raises(
        HTTPError,
        api.call_zendesk_api,
        "https://zccarchanazendeskcom.zendesk.com/",
    )


@responses.activate
def test_should_parse_valid_json():
    mock_uri = "https://zccarchanazendeskcom.zendesk.com/"
    f = open("test/test_data/test.json", "r")
    responses.add(
        responses.GET,
        mock_uri,
        status=200,
        json=json.load(f),
        content_type="application/json",
    )
    resp = api.get_tickets(mock_uri)
    len(resp) == 10


@responses.activate
def test_invalid_json_should_not_kill_app():
    mock_uri = "https://zccarchanazendeskcom.zendesk.com/"
    f = open("test/test_data/test_invalid.json", "r")
    responses.add(
        responses.GET,
        mock_uri,
        status=200,
        json=json.load(f),
        content_type="application/json",
    )
    pytest.raises(KeyError, api.get_tickets, mock_uri)
