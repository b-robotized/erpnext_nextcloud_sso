# nextcloud_sso (ERPNext v16)

Small Frappe app that adds a "userinfo shim" endpoint so ERPNext v16 can use Nextcloud's OAuth2
(which is not OpenID Connect and uses OCS APIs that need `OCS-APIRequest: true`).

## Install (bench)

0) Use the Frappe Marketplace or:

1) Copy/unzip this folder into your `frappe-bench/apps/` directory
2) Install on your site:

   bench --site <your-site> install-app erpnext_nextcloud_sso
   bench restart

## Configure ERPNext Social Login Key

**Good News:** This app adds "Nextcloud" as a built-in Social Login Provider option!

After installing the app:

1. **In Nextcloud**: Create an OAuth2 client (Admin → Security → OAuth 2.0) and set:
    - **Redirect URI**: `https://<your-erp>/api/method/erpnext_nextcloud_sso.oauth2_logins.login_via_nextcloud`

2.  **Create a new Social Login Key** (Integrations → Authentication → Social Login Key → New)

3.  **Select Provider**: Choose **"Nextcloud"** from the "Social Login Provider" dropdown
    - All OAuth endpoints, API endpoint, redirect URL, and icon are automatically filled in!

4.  **Fill in your instance-specific details**:
    - **Provider Name**: `<name or the provider` (e.g., `Nextcloud`) - this name will be shown on the login page
    - **Client ID**: (from Nextcloud OAuth2 client)
    - **Client Secret**: (from Nextcloud OAuth2 client)
    - **Base URL**: `https://<your-nextcloud>` (e.g., `https://cloud.example.com`)
    - **Enable Social Login**: Check box on top of the screen to activate the login button

5. **Save** the new Social Login Key entry.

6. **Go to login page** of your ERPnext by signing out or opening the URL `https://<your-erp>` in private tab.
   You should see there newly created login option marked with blue Nextcloud icon.

**Note**: The redirect URL uses the app's custom OAuth2 handler, providing a cleaner integration than the generic `/custom` endpoint.


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
