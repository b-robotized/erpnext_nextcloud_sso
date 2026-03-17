frappe.ui.form.on("Social Login Key", {
  social_login_provider(frm) {
    const fields = [
      "base_url",
      "authorize_url",
      "access_token_url",
      "api_endpoint",
      "client_id",
      "client_secret",
      "icon",
    ];
    for (var field of fields) {
      frm.set_df_property(field, "read_only", 0);
    }
  },
});
