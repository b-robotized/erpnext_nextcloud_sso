import frappe


def get_property_setters():
<<<<<<< HEAD
	"""
	Returns property setters to be applied during installation.
	
	This adds "Nextcloud" as an option to the Social Login Provider dropdown.
	"""
	# Get existing options from Social Login Key's social_login_provider field
	import frappe
	
	meta = frappe.get_meta("Social Login Key", cached=False)
	field = meta.get_field("social_login_provider")
	
	# Get current options (e.g., "Custom\nGoogle\nFacebook\n...")
	current_options = field.options or ""
	
	# Add Nextcloud if not already present
	if "Nextcloud" not in current_options:
		new_options = current_options.rstrip("\n") + "\nNextcloud"
	else:
		new_options = current_options
	
	return {
		"Social Login Key": [
			("social_login_provider", "options", new_options),
		],
	}
=======
    """
    Return property setters to be applied during installation.

    This adds "Nextcloud" as an option to the Social Login Provider dropdown.
    """
    # Get existing options from Social Login Key's social_login_provider field

    meta = frappe.get_meta("Social Login Key", cached=False)
    field = meta.get_field("social_login_provider")

    # Get current options (e.g., "Custom\nGoogle\nFacebook\n...")
    current_options = field.options or ""

    # Add Nextcloud if not already present
    if "Nextcloud" not in current_options:
        new_options = current_options.rstrip("\n") + "\nNextcloud"
    else:
        new_options = current_options

    return {
        "Social Login Key": [
            ("social_login_provider", "options", new_options),
        ],
    }
>>>>>>> f67ca19 (Addes stuff.)
