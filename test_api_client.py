import pytest 

from api_client import fetch_records

class FakeResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return [
            {
                "permit_number": "P-1001",
                "status": "issued",
            }
        ]
    
def test_fetch_records_returns_api_records(monkeypatch):
    def fake_get(endpoint, params, timeout):
        assert endpoint == "https://example.com/data.json"
        assert params == {
            "$limit": 25,
            "$offset": 50,
        }
        assert timeout == 5
        return FakeResponse()
    
    monkeypatch.setattr(
        "api_client.requests.get",
        fake_get,
    )

    result = fetch_records(
        "https://example.com/data.json",
        limit=25,
        offset=50,
        timeout=5,
    )
    assert result == [
        {
            "permit_number": "P-1001",
            "status": "issued",
        }
    ]   

