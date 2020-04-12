from app.application.models import User
from app.application.utils import get_md5
from tests.functional.helpers import web_test


@web_test
def test___repr__(context):
    user = User.create_user('ramadan', 'ramadan@test.io', 'pass1234')
    repr(user).should.equal('ramadan@test.io')


@web_test
def test_update_user(context):
    user = User.create_user('ramadan', 'ramadan@test.io', 'pass1234')
    user.update_user('ramadan1', 'ramadan1@test.io', 'pass11234')
    User.query.filter_by(email='ramadan@test.io').first().should.equal(None)
    updated_user = User.query.filter_by(email='ramadan1@test.io').first()
    updated_user.first_name.should.equal('ramadan1')
    updated_user.password.should.equal(get_md5('pass11234'))


@web_test
def test_to_dict(context):
    user = User.create_user('ramadan', 'ramadan@test.io', 'pass1234')
    user.to_dict().should.equal({
        'first_name': 'ramadan',
        'email': 'ramadan@test.io',
        'uuid': user.uuid,
    })


@web_test
def test_create_user(context):
    user = User.create_user('ramadan', 'ramadan@test.io', 'pass1234')
    user.first_name.should.equal('ramadan')
    user.email.should.equal('ramadan@test.io')
    user.password.should.equal(get_md5('pass1234'))
    User.query.filter_by(email='ramadan@test.io').first().shouldnot.equal(None)


@web_test
def test_delete_by_email(context):
    user = User.create_user('ramadan', 'ramadan@test.io', 'pass1234')
    User.delete_by_email('wrong').should.equal((False, {}))
    User.delete_by_email('ramadan@test.io').should.equal((True, {
        'first_name': 'ramadan',
        'email': 'ramadan@test.io',
        'uuid': user.uuid,
    }))
    User.query.filter_by(email='ramadan@test.io').first().should.equal(None)