from frappe.custom.doctype.customize_form.customize_form import (
    docfield_properties,
    doctype_properties,
)
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

from .property_setters import get_property_setters


def after_install():
    """
	Called after the app is installed on a site.

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
                if property_setter[0]:
                    for_doctype = False
                    property_type = docfield_properties[property_setter[1]]
                else:
                    for_doctype = True
                    property_type = doctype_properties[property_setter[1]]

                make_property_setter(
                    doctype=doctype,
                    fieldname=property_setter[0],
                    property=property_setter[1],
                    value=property_setter[2],
                    property_type=property_type,
                    for_doctype=for_doctype,
                )
