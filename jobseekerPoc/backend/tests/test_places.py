from unittest.mock import patch, MagicMock
from backend.places_service import fetch_nearby_companies, get_keywords_for_sectors
from backend.models import Company

def test_get_keywords():
    assert "software company" in get_keywords_for_sectors(["IT"])
    assert "hospital" in get_keywords_for_sectors(["Hospital"])
    assert "point_of_interest" == get_keywords_for_sectors([])

@patch('backend.places_service.requests.get')
def test_fetch_nearby_companies(mock_get):
    # Mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "results": [
            {
                "name": "Tech Corp",
                "vicinity": "123 Tech St",
                "geometry": {
                    "location": {"lat": 10.0, "lng": 20.0}
                },
                "place_id": "abc",
                "rating": 4.5,
                "types": ["point_of_interest", "establishment"]
            }
        ]
    }
    mock_get.return_value = mock_response

    companies = fetch_nearby_companies(10.0, 20.0, 5.0, ["IT"], "fake_key")

    assert len(companies) == 1
    assert isinstance(companies[0], Company)
    assert companies[0].name == "Tech Corp"
    assert companies[0].latitude == 10.0
    assert companies[0].longitude == 20.0

    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert kwargs['params']['key'] == "fake_key"
