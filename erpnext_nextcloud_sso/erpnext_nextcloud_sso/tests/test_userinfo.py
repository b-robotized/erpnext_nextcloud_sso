"""Unit tests for Nextcloud OAuth2 login functionality."""

import sys
from unittest.mock import MagicMock, patch

# Mock frappe module and its submodules before importing the app
sys.modules["frappe"] = MagicMock()
sys.modules["frappe.utils"] = MagicMock()
sys.modules["frappe.utils.oauth"] = MagicMock()
sys.modules["frappe.integrations"] = MagicMock()
sys.modules["frappe.integrations.oauth2_logins"] = MagicMock()
import frappe  # noqa: E402

# Configure frappe.whitelist to pass through the decorated function
frappe.whitelist = MagicMock(return_value=lambda f: f)

from erpnext_nextcloud_sso import oauth2_logins  # noqa: E402


def test_login_via_nextcloud():
    """Test that login_via_nextcloud calls login_via_oauth2 with correct params."""
    with patch.object(oauth2_logins, "login_via_oauth2") as mock_login:
        oauth2_logins.login_via_nextcloud("test_code", "test_state")
        mock_login.assert_called_once()
        args, kwargs = mock_login.call_args
        assert args[0] == "nextcloud"
        assert args[1] == "test_code"
        assert args[2] == "test_state"


def test_get_info_via_oauth_nextcloud():
    """Test extracting user info from Nextcloud OAuth response."""
    # Mock the OAuth flow and session
    mock_flow = MagicMock()
    mock_session = MagicMock()
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "ocs": {
            "data": {
                "email": "  Test@Example.com  ",
                "display-name": "Test User",
            }
        }
    }
    mock_session.get.return_value = mock_response
    mock_flow.get_auth_session.return_value = mock_session

    frappe.utils.oauth.get_oauth2_flow.return_value = mock_flow
    frappe.utils.oauth.get_oauth2_providers.return_value = {
        "nextcloud": {
            "api_endpoint": "https://cloud.example.com/api",
            "api_endpoint_args": {},
        }
    }
    frappe.utils.oauth.get_redirect_uri.return_value = "https://erp.example.com/callback"
    frappe.utils.oauth.get_email = MagicMock(return_value="test@example.com")

    # Call function
    result = oauth2_logins.get_info_via_oauth("nextcloud", "test_code")

    # Assertions - email should be normalized (lowercase, stripped)
    assert result["email"] == "test@example.com"
    assert result["name"] == "Test User"
    assert result["sub"] == "test@example.com"


def test_get_info_via_oauth_nextcloud_no_display_name():
    """Test that email is used as fallback name when display-name is missing."""
    mock_flow = MagicMock()
    mock_session = MagicMock()
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "ocs": {"data": {"email": "user@example.com"}}  # No display-name
    }
    mock_session.get.return_value = mock_response
    mock_flow.get_auth_session.return_value = mock_session

    frappe.utils.oauth.get_oauth2_flow.return_value = mock_flow
    frappe.utils.oauth.get_oauth2_providers.return_value = {
        "nextcloud": {
            "api_endpoint": "https://cloud.example.com/api",
            "api_endpoint_args": {},
        }
    }
    frappe.utils.oauth.get_redirect_uri.return_value = "https://erp.example.com/callback"
    frappe.utils.oauth.get_email = MagicMock(return_value="user@example.com")

    result = oauth2_logins.get_info_via_oauth("nextcloud", "test_code")

    # Email should be used as name fallback
    assert result["email"] == "user@example.com"
    assert result["name"] == "user@example.com"
    assert result["sub"] == "user@example.com"
