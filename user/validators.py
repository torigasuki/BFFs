import re


def email_validator(email):
    EMAIL_REGEX = EMAIL_REGEX = re.compile(
        r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
    )
    if not EMAIL_REGEX.match(email):
        return False
    else:
        return True
