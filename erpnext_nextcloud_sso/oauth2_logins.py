"""OAuth2 login handlers for Nextcloud SSO."""

import frappe
from frappe.utils.oauth import login_via_oauth2


@frappe.whitelist(allow_guest=True)
def login_via_nextcloud(code: str, state: str):
    """
    Handle OAuth2 callback from Nextcloud.

    This is called when Nextcloud redirects back to ERPNext after user authorization.
    The redirect URL is: /api/method/erpnext_nextcloud_sso.oauth2_logins.login_via_nextcloud
    """
    login_via_oauth2("nextcloud", code, state)
