import requests
import frappe


def _get_bearer_authorization() -> str:
    auth = frappe.get_request_header("Authorization") or ""
    auth = auth.strip()
    if not auth.lower().startswith("bearer "):
        frappe.throw("Missing Authorization: Bearer <token> header")
    return auth


def _get_nextcloud_base_url(provider: str) -> str:
    """
    Read Nextcloud base URL from the Social Login Key document in the ERPNext UI.

    We use the Social Login Key *document name* as provider (e.g. "Nextcloud").
    In the UI, set the Base URL to your Nextcloud root, e.g. https://cloud.example.com
    """
    try:
        doc = frappe.get_doc("Social Login Key", provider)
    except Exception:
        frappe.throw(f'Social Login Key "{provider}" not found.')

    # Field name is typically "base_url" in Frappe/ERPNext.
    nc_base = (getattr(doc, "base_url", None) or "").strip().rstrip("/")

    # Some setups leave Base URL empty; fail fast with a helpful message.
    if not nc_base:
        frappe.throw(f'Social Login Key "{provider}": Base URL is empty. Set it to your Nextcloud URL (e.g. https://cloud.example.com).')

    return nc_base


@frappe.whitelist(allow_guest=True)
def get(provider: str = "Nextcloud"):
    """
    Userinfo shim for Nextcloud OAuth2.

    Configure your Social Login Key like this:
      - Authorize URL: https://<nc>/apps/oauth2/authorize
      - Access Token URL: https://<nc>/apps/oauth2/api/v1/token
      - API Endpoint: https://<erp>/api/method/nextcloud_sso.userinfo.get?provider=Nextcloud
      - User ID Property: email

    ERPNext will call this endpoint with:
      Authorization: Bearer <access_token>

    We forward the token to Nextcloud's OCS endpoint adding:
      OCS-APIRequest: true
    and return a FLAT JSON object:
      { "email": "...", "name": "..." }
    """
    provider = (provider or "Nextcloud").strip()
    nc_base = _get_nextcloud_base_url(provider)
    auth = _get_bearer_authorization()

    # Nextcloud OCS "current user" endpoint (nested JSON)
    ocs_url = f"{nc_base}/ocs/v2.php/cloud/user?format=json"

    resp = requests.get(
        ocs_url,
        headers={
            "Authorization": auth,
            "OCS-APIRequest": "true",
            "Accept": "application/json",
        },
        timeout=15,
    )

    if resp.status_code >= 400:
        # Keep it short but useful; don't leak full bodies to the UI.
        body = (resp.text or "")[:300]
        frappe.throw(f"Nextcloud OCS user endpoint failed: {resp.status_code} {body}")

    payload = resp.json() or {}
    data = (payload.get("ocs") or {}).get("data") or {}

    email = (data.get("email") or "").strip().lower()
    name = (data.get("display-name") or data.get("displayname") or "").strip()

    if not email:
        frappe.throw("Nextcloud returned empty email. Ensure the user has an email set in Nextcloud (Profile settings).")

    if not name:
        name = email

    return {"email": email, "name": name}
