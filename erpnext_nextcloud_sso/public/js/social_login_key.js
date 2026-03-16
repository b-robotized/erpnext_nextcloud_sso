frappe.ui.form.on("Social Login Key", {
	social_login_provider(frm) {
		for (var field of fields) {
			frm.set_df_property(field, "read_only", 0);
		}
	}
});
