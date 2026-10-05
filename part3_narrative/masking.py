def alias_for(reseller_id):
    """
    Convert a reseller ID into a simple alias.
    """
    number = reseller_id.replace("RS", "")
    return f"ALIAS-{number}"


def assert_no_raw_names_leak(text, reseller_names):
    """
    Check whether any raw reseller name appears in the text.
    """
    for name in reseller_names:
        if name in text:
            return False

    return True