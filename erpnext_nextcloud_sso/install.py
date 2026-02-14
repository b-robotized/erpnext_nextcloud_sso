from frappe.custom.doctype.property_setter.property_setter import make_property_setter

from .property_setters import get_property_setters


def after_install():
    """
    Call after the app is installed on a site.

    This adds "Nextcloud" to the Social Login Provider dropdown.
    """
    apply_property_setters()


def apply_property_setters():
    """Apply property setters to extend DocType fields."""
    for doctypes, property_setters in get_property_setters().items():
        if isinstance(doctypes, str):
            doctypes = (doctypes,)

        for doctype in doctypes:
            for property_setter in property_setters:
                fieldname = property_setter[0]
                property_name = property_setter[1]
                value = property_setter[2]

                # Property type is determined automatically by make_property_setter
                make_property_setter(
                    doctype=doctype,
                    fieldname=fieldname,
                    property=property_name,
                    value=value,
                    property_type="Text",  # Options field is text type
                )
