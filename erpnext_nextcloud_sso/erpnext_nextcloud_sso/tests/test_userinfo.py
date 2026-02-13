import sys
from unittest.mock import MagicMock, patch

# Mock frappe module before importing the app
sys.modules["frappe"] = MagicMock()
import frappe

# Configure frappe.whitelist to pass through the decorated function
frappe.whitelist.return_value = lambda f: f

from erpnext_nextcloud_sso.erpnext_nextcloud_sso import userinfo

def test_get_bearer_authorization_valid():
    frappe.get_request_header.return_value = "Bearer valid_token"
    token = userinfo._get_bearer_authorization()
    assert token == "Bearer valid_token"

def test_get_bearer_authorization_invalid():
    frappe.get_request_header.return_value = "Basic something"
    
    # Reset mock side_effect from previous tests if any
    frappe.throw.side_effect = Exception("Throw called")
    
    try:
        userinfo._get_bearer_authorization()
    except Exception as e:
        assert str(e) == "Throw called"

@patch("erpnext_nextcloud_sso.erpnext_nextcloud_sso.userinfo.requests.get")
def test_userinfo_get_success(mock_get):
    # Setup mocks
    frappe.get_request_header.return_value = "Bearer token"
    
    mock_doc = MagicMock()
    mock_doc.base_url = "https://cloud.example.com"
    frappe.get_doc.return_value = mock_doc
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "ocs": {
            "data": {
                "email": "test@example.com",
                "display-name": "Test User"
            }
        }
    }
    mock_get.return_value = mock_response

    # Call function
    result = userinfo.get("Nextcloud")

    # Assertions
    assert result["email"] == "test@example.com"
    assert result["name"] == "Test User"
    
    # Verify calls
    frappe.get_doc.assert_called_with("Social Login Key", "Nextcloud")
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert args[0] == "https://cloud.example.com/ocs/v2.php/cloud/user?format=json"
    assert kwargs["headers"]["Authorization"] == "Bearer token"
