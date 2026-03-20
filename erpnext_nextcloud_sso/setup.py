import frappe


def add_nextcloud_provider():
    df = frappe.get_meta("Social Login Key").get_field("social_login_provider")

    if not df:
        return

    options = df.options.split("\n") if df.options else []

    if "Nextcloud" not in options:
        options.append("Nextcloud")

        frappe.db.set_value(
            "DocField",
            {"parent": "Social Login Key", "fieldname": "social_login_provider"},
            "options",
            "\n".join(options),
        )

        frappe.clear_cache()


def remove_nextcloud_provider():
    df = frappe.get_meta("Social Login Key").get_field("social_login_provider")

    if not df:
        return

    options = df.options.split("\n") if df.options else []
    if "Nextcloud" not in options:
        return

    options = [option for option in options if option != "Nextcloud"]

    frappe.db.set_value(
        "DocField",
        {"parent": "Social Login Key", "fieldname": "social_login_provider"},
        "options",
        "\n".join(options),
    )

    frappe.clear_cache()
