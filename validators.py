import re

def validate_phone(phone):
    """Validate that the phone number consists of exactly 10 digits."""
    return phone.isdigit() and len(phone) == 10

def validate_name(name):
    """Validate that the name contains only letters and spaces."""
    return re.match("^[A-Za-z\s]+$", name) is not None