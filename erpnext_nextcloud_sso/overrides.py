"""Override Frappe's Social Login Key to add Nextcloud provider."""

import json

import frappe
from frappe.integrations.doctype.social_login_key.social_login_key import SocialLoginKey


class CustomSocialLoginKey(SocialLoginKey):
    """
    Extend Social Login Key to add Nextcloud as a recognized provider.

    This class overrides the get_social_login_provider method.
    """

    def get_social_login_provider(self, provider, initialize=False):
        """
        Override to add Nextcloud provider configuration.

        If provider is "Nextcloud", return pre-configured settings.
        Otherwise, delegate to parent class.
        """
        if provider == "Nextcloud":
            # Get the current site URL for absolute API endpoint
            site_url = frappe.utils.get_url()

            return {
                "provider_name": "Nextcloud",
                "custom_base_url": 1,
                "icon": "/assets/erpnext_nextcloud_sso/nextcloud.svg",
                "redirect_url": (
                    "/api/method/erpnext_nextcloud_sso.oauth2_logins.login_via_nextcloud"
                ),
                # API endpoint must be absolute URL pointing to ERPNext, not Nextcloud
                "api_endpoint": (
                    f"{site_url}/api/method/erpnext_nextcloud_sso.erpnext_nextcloud_sso"
                    ".userinfo.get?provider=nextcloud"
                ),
                "authorize_url": "/apps/oauth2/authorize",
                "access_token_url": "/apps/oauth2/api/v1/token",
                "auth_url_data": json.dumps({"response_type": "code", "scope": ""}),
            }

        # For all other providers, use the parent class method
        return super().get_social_login_provider(provider, initialize)
