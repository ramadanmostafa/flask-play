import re
from collections import defaultdict
from typing import List, Dict

from app.application.models import User

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


def validate_email_format(email: str) -> (bool, str):
    if not EMAIL_REGEX.match(email):
        return False, 'Invalid Email format.'
    return True, ''


def validate_email_already_exists(email: str):
    if User.query.filter_by(email=email).first():
        return False, 'Email already exists.'
    return True, ''


def validate_field_required(val):
    if val in [None, '']:
        return False, 'This field is required'
    return True, ''


def run_validators(validators: List[Dict]) -> (bool, dict):
    """
    get a list of objects, each object should have the keys
    (field_name: contains the field name, field_val: contains the actual value of the field
    func: is the validator function will be called)
    :param validators:
    :return: errors dictionary in the format {field1: [err1, err2]}
    """
    errors = defaultdict(lambda: [])
    for validator_obj in validators:
        is_valid, error_message = validator_obj['func'](validator_obj['field_val'])
        if not is_valid:
            errors[validator_obj['field_name']].append(error_message)

    return errors
