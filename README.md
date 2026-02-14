# nextcloud_sso (ERPNext v16)

Small Frappe app that adds a "userinfo shim" endpoint so ERPNext v16 can use Nextcloud's OAuth2
(which is not OpenID Connect and uses OCS APIs that need `OCS-APIRequest: true`).

## Install (bench)

1) Copy/unzip this folder into your `frappe-bench/apps/` directory
2) Install on your site:

   bench --site <your-site> install-app nextcloud_sso
   bench restart

## Configure ERPNext Social Login Key

**IMPORTANT:** Use **lowercase** for the Social Login Key **Name** (ID field). The **Label** (display name) can be Title Case.

Create a Social Login Key:
- **Name (ID)**: `nextcloud` (lowercase - this is used in URLs and must match Nextcloud OAuth configuration)
- **Label** (optional): `Nextcloud` (Title Case - this is what appears on the login button)
- **Icon**: `/assets/erpnext_nextcloud_sso/nextcloud.svg` (optional - displays the Nextcloud logo on the login button)

Configuration fields:
- Authorize URL: `https://<nc>/apps/oauth2/authorize`
- Access Token URL: `https://<nc>/apps/oauth2/api/v1/token`
- Base URL: `https://<nc>` (set this in the UI; no site_config needed)
- API Endpoint: `https://<erp>/api/method/erpnext_nextcloud_sso.erpnext_nextcloud_sso.userinfo.get?provider=nextcloud`
- User ID Property: `email`
- Auth URL Data: `{"response_type":"code","scope":""}`

In Nextcloud, create an OAuth2 client and set Redirect URI to:
`https://<erp>/api/method/frappe.integrations.oauth2_logins.custom/nextcloud`

**Note**: All URLs use lowercase `nextcloud` to match the Social Login Key Name field.


## Testing

### 1. Unit Tests (Logic Verification)
These tests check the Python code logic (e.g. `userinfo.py`) in isolation. They are fast and run locally or in CI without a full Frappe environment.

**Run locally:**
```bash
docker run --rm -v $(pwd):/app -w /app python:3.14-slim \
    bash -c "pip install -e . pytest && pytest erpnext_nextcloud_sso/erpnext_nextcloud_sso/tests"
```

### 2. Integration Tests (Installation Verification)
These tests verify that the app can be successfully installed into a real ERPNext site using Docker Compose.

**Automated Management Script:**
I have provided a helper script to manage the lifecycle of your test environment.

1.  **Start Clean & Run**:
    This will clean up previous runs, build the image, start the containers, and show the installation logs.
    ```bash
    ./manage.sh
    ```

2.  **Clean Up Only**:
    This will stop containers and remove all volumes and images created by this test, freeing up space.
    ```bash
    ./manage.sh --clean-only
    ```

**Manual Commands:**
If you prefer running commands manually:
```bash
cd docker
docker compose up -d --build
docker compose logs -f configurator
```
