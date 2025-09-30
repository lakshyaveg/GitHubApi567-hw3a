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
    # Arrange: responses for repos list then commits for two repos
    get.side_effect = [
        mock_response([{"name": "A"}, {"name": "B"}]),  # list repos
        mock_response([{"sha": "x"}]),                  # commits for A
        mock_response([{"sha": "y"}, {"sha": "z"}]),    # commits for B
    ]

    # Act: call public function to list repos, then use the module's _get_json
    # to fetch commits (still goes through requests.get under the hood)
    names = gh.list_user_repos("user123")
    assert names == ["A", "B"]

    cnt_a = len(gh._get_json("https://api.github.com/repos/user123/A/commits"))
    cnt_b = len(gh._get_json("https://api.github.com/repos/user123/B/commits"))

    # Assert counts and exact URLs requested (order matters)
    assert cnt_a == 1 and cnt_b == 2

    expected = [
        call("https://api.github.com/users/user123/repos", timeout=15),
        call("https://api.github.com/repos/user123/A/commits", timeout=15),
        call("https://api.github.com/repos/user123/B/commits", timeout=15),
    ]
    assert get.call_args_list == expected
