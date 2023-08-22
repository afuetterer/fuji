"""
A collection of tests to test the reponses of a Fask tesk fuji client,
i.e. if the app is working and there are no swagger problems.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask.testing import FlaskClient

HTTP_200_OK = 200
HTTP_404_NOT_FOUND = 404


def test_ui_returns_200(client: "FlaskClient") -> None:
    """Basic smoke test to see if app is buildable"""
    valid_url = "/fuji/api/v1/ui/"
    response = client.get(valid_url)
    assert response.status_code == HTTP_200_OK


# pytest param
# metric 1,2,3,4...

def test_get_metrics(client: "FlaskClient") -> None:
    """Test if a client get returns the metric"""
    url = "/fuji/api/v1/metrics/0.5"
    response = client.get(url)
    assert response.status_code == HTTP_200_OK

    result = response.json

    print(result.keys())

    metrics = result["metrics"]
    assert isinstance(metrics, list)
    total = result["total"]
    print(total)

    NUM_METRICS = 17
    assert total == NUM_METRICS


# http://localhost:1071/fuji/api/v1/metrics/0.4
# http://localhost:1071/fuji/api/v1/metrics/0.5

# http://localhost:1071/fuji/api/v1/ui

# /evaluate
# /metrics/{version}
# /metrics/{version}/{metric}
# /harvest
