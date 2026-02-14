app_name = 'erpnext_nextcloud_sso'
app_title = 'Nextcloud SSO'
app_publisher = 'b»robotized group'
app_description = 'Userinfo shim to use Nextcloud OAuth2 with ERPNext v16 social login.'
app_email = 'erp-devs@b-robotized.com'
app_license = 'MIT'

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/erpnext_nextcloud_sso/css/erpnext_nextcloud_sso.css"
app_include_js = "/assets/erpnext_nextcloud_sso/js/erpnext_nextcloud_sso.js"

# Installation
# ------------

after_install = "erpnext_nextcloud_sso.install.after_install"

# Override Methods
# ----------------

override_whitelisted_methods = {
	"frappe.integrations.doctype.social_login_key.social_login_key.get_social_login_provider": "erpnext_nextcloud_sso.overrides.get_social_login_provider"
}
