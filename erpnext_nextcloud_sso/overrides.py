import json
import frappe


@frappe.whitelist()
def get_social_login_provider(provider: str, initialize: bool = True) -> dict:
    """
    Override Frappe's get_social_login_provider to add Nextcloud.

    This adds "Nextcloud" as a recognized social login provider with pre-configured settings.
    """
    # Import the original function
    from frappe.integrations.doctype.social_login_key.social_login_key import (
        get_social_login_provider as original_get_social_login_provider,
    )

    # If requesting Nextcloud provider configuration, return our settings
    if provider == "Nextcloud":
        return {
            "provider_name": "Nextcloud",
            "custom_base_url": 1,
            "icon": "/assets/erpnext_nextcloud_sso/nextcloud.svg",
            "redirect_url": "/api/method/frappe.integrations.oauth2_logins.custom/nextcloud",
            "api_endpoint": "/api/method/erpnext_nextcloud_sso.erpnext_nextcloud_sso.userinfo.get?provider=nextcloud",
            "authorize_url": "/apps/oauth2/authorize",
            "access_token_url": "/apps/oauth2/api/v1/token",
            "auth_url_data": json.dumps({"response_type": "code", "scope": ""}),
        }

    # For all other providers, use the original function
    return original_get_social_login_provider(provider, initialize)
