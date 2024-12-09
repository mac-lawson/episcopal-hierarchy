import re

def transform_titles(titles):
    transformed = []

    for title in titles:
        title = title.strip()  # Remove any leading/trailing whitespace

        # Match cases with parentheses
        match_with_parentheses = re.match(r"^(.*)\((.*?)\)$", title)
        if match_with_parentheses:
            state, role = match_with_parentheses.groups()
            transformed.append(f"{role.strip()} Bishop of {state.strip()}")
        else:
            # Ensure "Bishop" is included in the default case
            match_default = re.match(r"^(.*?)([A-Za-z ]+)$", title)
            if match_default:
                transformed.append(f"Bishop of {match_default.group(2).strip()}")

    return transformed



