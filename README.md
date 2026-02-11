# nextcloud_sso (ERPNext v16)

Small Frappe app that adds a "userinfo shim" endpoint so ERPNext v16 can use Nextcloud's OAuth2
(which is not OpenID Connect and uses OCS APIs that need `OCS-APIRequest: true`).

## Install (bench)

1) Copy/unzip this folder into your `frappe-bench/apps/` directory
2) Install on your site:

   bench --site <your-site> install-app nextcloud_sso
   bench restart

## Configure ERPNext Social Login Key

Create a Social Login Key named **Nextcloud** (or any name you prefer; use the same in `provider=` below).

- Authorize URL: https://<nc>/apps/oauth2/authorize
- Access Token URL: https://<nc>/apps/oauth2/api/v1/token
- Base URL: https://<nc>     (set this in the UI; no site_config needed)
- API Endpoint: https://<erp>/api/method/nextcloud_sso.userinfo.get?provider=Nextcloud
- User ID Property: email
- Auth URL Data: {"response_type":"code","scope":""}

In Nextcloud, create an OAuth2 client and set Redirect URI to:
  https://<erp>/api/method/frappe.integrations.oauth2_logins.custom/Nextcloud
