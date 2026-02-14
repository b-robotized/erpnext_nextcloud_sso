# nextcloud_sso (ERPNext v16)

Small Frappe app that adds a "userinfo shim" endpoint so ERPNext v16 can use Nextcloud's OAuth2
(which is not OpenID Connect and uses OCS APIs that need `OCS-APIRequest: true`).

## Install (bench)

1) Copy/unzip this folder into your `frappe-bench/apps/` directory
2) Install on your site:

   bench --site <your-site> install-app nextcloud_sso
   bench restart

## Configure ERPNext Social Login Key

**Good News:** This app adds "Nextcloud" as a built-in Social Login Provider option!

After installing the app:

1.  **Create a new Social Login Key** (Integrations → Authentication → Social Login Key → New)

2.  **Select Provider**: Choose **"Nextcloud"** from the "Social Login Provider" dropdown
    - All OAuth endpoints, API endpoint, and icon are automatically filled in!

3.  **Fill in your instance-specific details**:
    - **Name**: `nextcloud` (lowercase - used in URLs)
    - **Base URL**: `https://<your-nextcloud>` (e.g., `https://cloud.example.com`)
    - **Client ID**: (from Nextcloud OAuth2 client)
    - **Client Secret**: (from Nextcloud OAuth2 client)
    - **Enable Social Login**: Check this box to activate the login button

2.  **In Nextcloud**: Create an OAuth2 client (Admin → Security → OAuth 2.0) and set:
    - **Redirect URI**: `https://<your-erp>/api/method/frappe.integrations.oauth2_logins.custom/nextcloud`

**Note**: All URLs use lowercase `nextcloud` to match the Social Login Key Name field. The button label will show "Nextcloud" (Title Case).


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
