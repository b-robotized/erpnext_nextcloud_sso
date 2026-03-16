"""OAuth2 login handlers for Nextcloud SSO."""

import frappe
from frappe.utils.oauth import login_oauth_user
from frappe.integrations.oauth2_logins import decoder_compat
from frappe import _
import json
import jwt
from collections.abc import Callable


@frappe.whitelist(allow_guest=True)
def login_via_nextcloud(code: str, state: str):
    """
    Handle OAuth2 callback from Nextcloud.

    This is called when Nextcloud redirects back to ERPNext after user authorization.
    The redirect URL is: /api/method/erpnext_nextcloud_sso.oauth2_logins.login_via_nextcloud
    """

    login_via_oauth2("nextcloud", code, state, decoder=decoder_compat)


def login_via_oauth2(provider: str, code: str, state: str, decoder: Callable | None = None):
    info = get_info_via_oauth(provider, code, decoder)
    login_oauth_user(info, provider=provider, state=state)


def get_info_via_oauth(
    provider: str, code: str, decoder: Callable | None = None, id_token: bool = False
):
    flow = frappe.utils.oauth.get_oauth2_flow(provider)
    oauth2_providers = frappe.utils.oauth.get_oauth2_providers()

    args = {
        "data": {
            "code": code,
            "redirect_uri": frappe.utils.oauth.get_redirect_uri(provider),
            "grant_type": "authorization_code",
        }
    }

    if decoder:
        args["decoder"] = decoder

    session = flow.get_auth_session(**args)

    if id_token:
        parsed_access = json.loads(session.access_token_response.text)
        token = parsed_access["id_token"]
        info = jwt.decode(token, flow.client_secret, options={"verify_signature": False})
    else:
        api_endpoint = oauth2_providers[provider].get("api_endpoint")
        api_endpoint_args = oauth2_providers[provider].get("api_endpoint_args")

        info = session.get(api_endpoint, params=api_endpoint_args).json()

        if provider == "nextcloud":
            info = info.get("ocs", {}).get("data", {})
            email = (info.get("email") or "").strip().lower()
            name = (info.get("display-name") or info.get("displayname") or "").strip()
            info["email"] = email
            info["name"] = name or email
            info["sub"] = email

    if not (
        info.get("email_verified") or frappe.utils.oauth.get_email(info)
    ):  # Use original helper
        frappe.throw(_("Email not verified with {0}").format(provider.title()))

    return info