from django import template

register = template.Library()

# Mapping of English digits to Persian digits
EN_TO_FA_NUMBERS = {
    "0": "۰",
    "1": "۱",
    "2": "۲",
    "3": "۳",
    "4": "۴",
    "5": "۵",
    "6": "۶",
    "7": "۷",
    "8": "۸",
    "9": "۹",
}


@register.filter(name="en_to_fa")
def en_to_fa(value):
    """
    Convert English digits in a string to Persian digits.

    Args:
        value (str): The input text containing English digits.

    Returns:
        str: The text with English digits replaced by Persian digits.
    """
    if not isinstance(value, str):
        value = str(value)
    # Replace each character if it is a digit, otherwise keep it
    return "".join(EN_TO_FA_NUMBERS.get(ch, ch) for ch in value)
