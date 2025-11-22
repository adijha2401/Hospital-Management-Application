# small set of validators for backend use
from email_validator import validate_email, EmailNotValidError

def validate_email_address(email):
    try:
        v = validate_email(email)
        return v.email
    except EmailNotValidError:
        return None
