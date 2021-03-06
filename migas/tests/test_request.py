import pytest

from migas.config import DEFAULT_ENDPOINT, DEFAULT_ROOT
from migas.request import request

POST_QUERY = 'query{get_usage{project:"git/hub",start:"2022-07-01"}}'


@pytest.mark.parametrize(
    'endpoint,query,method', [(DEFAULT_ENDPOINT, POST_QUERY, "POST"), (DEFAULT_ROOT, None, "GET")]
)
def test_request(endpoint, query, method):
    status, res = request(endpoint, query=query, method=method)
    assert status == 200
    assert res


def test_timeout(monkeypatch):
    status, res = request(DEFAULT_ROOT, timeout=0.00001, method="GET")
    assert status == 408
    assert res['errors']

    monkeypatch.setenv('MIGAS_TIMEOUT', '0.000001')
    status, res = request(DEFAULT_ROOT, method="GET")
    assert status == 408
    assert res['errors']
