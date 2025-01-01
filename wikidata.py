import wptools

def holy_orders(name): 
    """Get Wikipedia data for a specific bishop."""
    try:
        so = wptools.page(str(name)).get_parse()
        infobox = so.data['infobox']
        # Attempt to access the key 'ordination', fallback to "Unknown" if it doesn't exist
        return infobox.get("ordination")
    except (KeyError, TypeError, LookupError):
        return "Unknown"

def p_consecrator(name): 
    """Get Wikipedia data for a specific bishop."""
    try:
        so = wptools.page(str(name)).get_parse()
        infobox = so.data['infobox']
        # Attempt to access the key 'ordination', fallback to "Unknown" if it doesn't exist
        return infobox.get("ordination")
    except (KeyError, TypeError, LookupError):
        return "Unknown"

