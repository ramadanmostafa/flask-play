from app.application.models import User
from app.application.validators import validate_email_format, validate_email_already_exists, validate_field_required, \
    run_validators
from tests.functional.helpers import web_test


def test_validate_email_format():
    is_valid, err_msg = validate_email_format('test')
    is_valid.should.equal(False)
    err_msg.should.equal('Invalid Email format.')

    is_valid, err_msg = validate_email_format('test@test.io')
    is_valid.should.equal(True)
    err_msg.should.equal('')

    is_valid, err_msg = validate_email_format('test@test')
    is_valid.should.equal(False)
    err_msg.should.equal('Invalid Email format.')


@web_test
def test_validate_email_already_exists(context):
    User.create_user('test', 'test@test.io', 'test')
    is_valid, err_msg = validate_email_already_exists('test@test.io')
    is_valid.should.equal(False)
    err_msg.should.equal('Email already exists.')

    is_valid, err_msg = validate_email_already_exists('test1@test.io')
    is_valid.should.equal(True)
    err_msg.should.equal('')


def test_validate_field_required():
    is_valid, err_msg = validate_field_required('')
    is_valid.should.equal(False)
    err_msg.should.equal('This field is required')

    is_valid, err_msg = validate_field_required('test@test.io')
    is_valid.should.equal(True)
    err_msg.should.equal('')

    is_valid, err_msg = validate_field_required(None)
    is_valid.should.equal(False)
    err_msg.should.equal('This field is required')


@web_test
def test_run_validators(context):
    test_data = [
        {'validators': [], 'errors': {}},
        {
            'validators': [
                {'field_name': 'test', 'field_val': 'test', 'func': validate_email_already_exists},
                {'field_name': 'test', 'field_val': 'test', 'func': validate_field_required},
                {'field_name': 'test', 'field_val': 'test', 'func': validate_email_format},
            ],
            'errors': {
                'test': ['Invalid Email format.']
            }
        },
        {
            'validators': [
                {'field_name': 'test', 'field_val': '', 'func': validate_email_already_exists},
                {'field_name': 'test', 'field_val': '', 'func': validate_field_required},
                {'field_name': 'test', 'field_val': '', 'func': validate_email_format},
            ],
            'errors': {
                'test': ['This field is required', 'Invalid Email format.']
            }
        },
        {
            'validators': [
                {'field_name': 'test1', 'field_val': '', 'func': validate_email_already_exists},
                {'field_name': 'test2', 'field_val': '', 'func': validate_field_required},
                {'field_name': 'test3', 'field_val': '', 'func': validate_email_format},
            ],
            'errors': {
                'test2': ['This field is required'],
                'test3': ['Invalid Email format.']
            }
        },
    ]
    for item in test_data:
        errors = run_validators(item['validators'])
        errors.should.equal(item['errors'])
