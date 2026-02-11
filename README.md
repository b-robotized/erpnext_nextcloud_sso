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

## Testing

### 1. Unit Tests (Logic Verification)
These tests check the Python code logic (e.g. `userinfo.py`) in isolation. They are fast and run locally or in CI without a full Frappe environment.

**Run locally:**
```bash
docker run --rm -v $(pwd):/app -w /app python:3.14-slim \
    bash -c "pip install -e . pytest && pytest erpnext_nextcloud_sso/tests"
```

### 2. Integration Tests (Installation Verification)
These tests verify that the app can be successfully installed into a real ERPNext site. They run using Docker Compose.

**Prerequisite:**
You must push your code to GitHub first. The `Build Container Image` workflow will run and publish the Docker image `ghcr.io/b-robotized/erpnext_nextcloud_sso:stable`.

**Run locally:**
```bash
cd docker
docker compose up -d
docker compose logs -f configurator
```

*   The `configurator` service attempts to create a new site and run `install-app erpnext_nextcloud_sso`.
*   If you see "Setup completed" in the logs, the app is successfully installable.
*   If it fails, the logs will show why the installation was rejected.
