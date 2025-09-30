from unittest.mock import patch, call, Mock
import src.gh_api as gh

def mock_response(json_data, status=200, headers=None):
    m = Mock()
    m.status_code = status
    m.json.return_value = json_data
    m.headers = headers or {}
    m.text = "error"
    return m

@patch("requests.get")  # patch global requests.get so no real HTTP happens
def test_never_calls_network_directly(get):
    # Arrange: responses for list-repos, commits for A, commits for B
    get.side_effect = [
        mock_response([{"name": "A"}, {"name": "B"}]),
        mock_response([{"sha": "x"}]),
        mock_response([{"sha": "y"}, {"sha": "z"}]),
    ]

    # Act using only gh._get_json (which calls requests.get under the hood)
    repos = gh._get_json("https://api.github.com/users/user123/repos")
    names = [r["name"] for r in repos]
    cnt_a = len(gh._get_json("https://api.github.com/repos/user123/A/commits"))
    cnt_b = len(gh._get_json("https://api.github.com/repos/user123/B/commits"))

    # Assert results
    assert names == ["A", "B"]
    assert cnt_a == 1 and cnt_b == 2

    # Assert exact URLs requested in order
    expected = [
        call("https://api.github.com/users/user123/repos", timeout=15),
        call("https://api.github.com/repos/user123/A/commits", timeout=15),
        call("https://api.github.com/repos/user123/B/commits", timeout=15),
    ]
    assert get.call_args_list == expected
