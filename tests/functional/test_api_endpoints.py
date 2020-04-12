import hashlib
import json

from app.application.models import User
from .helpers import web_test


# This test suite uses the python module "sure":
#
# https://sure.readthedocs.io/en/latest/api-reference.html#example-setup-a-flask-app-for-testing


@web_test
def test_index_page(context):
    ("GET on / should render an HTML page")

    # Given that I perform a GET /
    response = context.http.get("/")

    # Then check if the status was 200
    response.status_code.should.equal(200)

    # And when I check the content type is html
    response.headers.should.have.key("Content-Type")

    # Then it should be html
    response.headers["Content-Type"].should.contain("text/html")


@web_test
def test_hello_world(context):
    ("GET on /api/example should return a json containing hello world")

    # Given that I perform a GET /api/example
    response = context.http.get("/api/example")

    # When I check the response
    response.headers.should.have.key("Content-Type").being.equal("application/json")

    # And check if the status was 200
    response.status_code.should.equal(200)

    # And when I deserialize the JSON
    data = json.loads(response.data)

    # Then the data should have the key "hello" with value "world"
    data.should.have.key("hello").being.equal("world")


@web_test
def test_api_calculate_md5_invalid(context):
    ("POST on /api/calculate-md5 with wrong key")
    response = context.http.post(
        "/api/calculate-md5",
        data=json.dumps({'data1': 'email@OK.com'}),
        content_type='application/json'
    )
    response.headers.should.have.key("Content-Type").being.equal("application/json")
    response.status_code.should.equal(400)
    data = json.loads(response.data)
    data.should.have.key("data").being.equal(["This field is required"])


@web_test
def test_api_calculate_md5_valid(context):
    ("POST on /api/calculate-md5 with valid data")
    response = context.http.post(
        "/api/calculate-md5",
        data=json.dumps({'data': 'email@OK.com'}),
        content_type='application/json',
    )
    response.headers.should.have.key("Content-Type").being.equal("application/json")
    response.status_code.should.equal(200)
    data = json.loads(response.data)
    data.should.have.key("md5").being.equal('4a311b40964e7f6372a253081f8c61f2')


@web_test
def test_api_create_user_invalid(context):
    ("POST on /api/user missing_data")
    response = context.http.post("/api/user")
    response.headers.should.have.key("Content-Type").being.equal("application/json")
    response.status_code.should.equal(400)
    data = json.loads(response.data)
    data.should.have.key("first_name").being.equal(["This field is required"])
    data.should.have.key("email").being.equal(["This field is required", 'Invalid Email format.'])
    data.should.have.key("password").being.equal(["This field is required"])


@web_test
def test_api_create_user_email_exists(context):
    ("POST on /api/user email already exists")
    User.create_user('ramadan2', 'ramadan@thebest.com', 'pass12344')
    response = context.http.post(
        "/api/user",
        data=json.dumps({'first_name': 'ramadan', 'email': 'ramadan@thebest.com', 'password': 'pass1234'}),
        content_type='application/json',
    )
    response.headers.should.have.key("Content-Type").being.equal("application/json")
    response.status_code.should.equal(400)
    data = json.loads(response.data)
    data.should.have.key("email").being.equal(['Email already exists.'])


@web_test
def test_api_create_user_valid(context):
    ("POST on /api/user valid data")
    response = context.http.post(
        "/api/user",
        data=json.dumps({'first_name': 'ramadan', 'email': 'ramadan2@thebest.com', 'password': 'pass1234'}),
        content_type='application/json',
    )
    response.headers.should.have.key("Content-Type").being.equal("application/json")
    response.status_code.should.equal(200)
    data = json.loads(response.data)
    data.should.have.key("first_name").being.equal("ramadan")
    data.should.have.key("email").being.equal("ramadan2@thebest.com")
    data.should.have.key("uuid").being.equal(
        hashlib.md5("ramadan:ramadan2@thebest.com".encode()).hexdigest()
    )


@web_test
def test_api_retrieve_user_valid(context):
    ("GET on /api/user/<uuid> with valid uuid")
    user = User.create_user('ramadan2', 'ramadan@thebest.com', 'pass12344')
    response = context.http.get("/api/user/{}".format(user.uuid))
    response.status_code.should.equal(200)
    data = json.loads(response.data)
    data.should.have.key("first_name").being.equal(user.first_name)
    data.should.have.key("email").being.equal(user.email)
    data.should.have.key("uuid").being.equal(
        user.uuid
    )


@web_test
def test_api_retrieve_user_wrong_uuid(context):
    ("GET on /api/user/<uuid> with wrong uuid")
    response = context.http.get("/api/user/wrong")
    response.status_code.should.equal(404)


@web_test
def test_api_update_user_wrong_uuid(context):
    ("PUT on /api/user/<uuid> with wrong uuid")
    response = context.http.put("/api/user/wrong")
    response.status_code.should.equal(404)


@web_test
def test_api_update_user_valid(context):
    ("PUT on /api/user/<uuid> with valid data")
    user = User.create_user('ramadan2', 'ramadan@thebest.com', 'pass12344')
    response = context.http.put(
        "/api/user/{}".format(user.uuid),
        data=json.dumps({'first_name': 'ramadan3', 'email': 'ramadan3@thebest.com', 'password': 'password'}),
        content_type='application/json',
    )
    response.status_code.should.equal(200)
    data = json.loads(response.data)
    data.should.have.key("first_name").being.equal('ramadan3')
    data.should.have.key("email").being.equal('ramadan3@thebest.com')
    data.should.have.key("uuid").being.equal(
        user.uuid
    )


@web_test
def test_api_update_user_password_valid(context):
    ("PUT on /api/user/<uuid> update user password")
    user = User.create_user('ramadan2', 'ramadan@thebest.com', 'pass12344')
    response = context.http.put(
        "/api/user/{}".format(user.uuid),
        data=json.dumps({'password': 'password'}),
        content_type='application/json',
    )
    response.status_code.should.equal(200)
    data = json.loads(response.data)
    data.should.have.key("first_name").being.equal('ramadan2')
    data.should.have.key("email").being.equal('ramadan@thebest.com')
    data.should.have.key("uuid").being.equal(
        user.uuid
    )


@web_test
def test_api_update_user_first_name_valid(context):
    ("PUT on /api/user/<uuid> update first name")
    user = User.create_user('ramadan2', 'ramadan@thebest.com', 'pass12344')
    response = context.http.put(
        "/api/user/{}".format(user.uuid),
        data=json.dumps({'first_name': 'ramadan khalifa'}),
        content_type='application/json',
    )
    response.status_code.should.equal(200)
    data = json.loads(response.data)
    data.should.have.key("first_name").being.equal('ramadan khalifa')
    data.should.have.key("email").being.equal('ramadan@thebest.com')
    data.should.have.key("uuid").being.equal(
        user.uuid
    )
    User.query.filter_by(email='ramadan@thebest.com').first().first_name.should.equal('ramadan khalifa')


@web_test
def test_api_update_user_invalid_email(context):
    ("PUT on /api/user/<uuid> invalid email")
    user = User.create_user('ramadan2', 'ramadan@thebest.com', 'pass12344')
    response = context.http.put(
        "/api/user/{}".format(user.uuid),
        data=json.dumps({'first_name': 'ramadan3', 'email': 'ramadan3', 'password': 'password'}),
        content_type='application/json',
    )
    response.status_code.should.equal(400)
    data = json.loads(response.data)
    data.should.have.key("email").being.equal(['Invalid Email format.'])


@web_test
def test_api_update_user_email_already_exists(context):
    ("PUT on /api/user/<uuid> email already exists")
    User.create_user('ramadan2', 'ramadan22@thebest.com', 'pass12344')
    user = User.create_user('ramadan2', 'ramadan@thebest.com', 'pass12344')
    response = context.http.put(
        "/api/user/{}".format(user.uuid),
        data=json.dumps({'first_name': 'ramadan3', 'email': 'ramadan22@thebest.com', 'password': 'password'}),
        content_type='application/json',
    )
    response.status_code.should.equal(400)
    data = json.loads(response.data)
    data.should.have.key("email").being.equal(['Email already exists.'])


@web_test
def test_api_list_users(context):
    ("GET on /api/users list all users")
    User.create_user('ramadan2', 'ramadan22@thebest.com', 'pass12344')
    User.create_user('ramadan2', 'ramadan@thebest.com', 'pass12344')
    response = context.http.get("/api/users")
    response.status_code.should.equal(200)
    data = json.loads(response.data)
    data.should.equal(
        [{'first_name': 'ramadan2', 'email': 'ramadan22@thebest.com', 'uuid': '13fcf48d5e398eda1f6ec6531c927ab2'},
         {'first_name': 'ramadan2', 'email': 'ramadan@thebest.com', 'uuid': 'f9558794ccfab66c8b49f17c93eeae8e'}]
    )


@web_test
def test_api_list_users_empty(context):
    ("GET on /api/users list all users when there is no users")
    response = context.http.get("/api/users")
    response.status_code.should.equal(200)
    data = json.loads(response.data)
    data.should.equal([])


@web_test
def test_api_delete_user_wrong_email(context):
    ("DELETE on /api/user/<email> with wrong email")
    response = context.http.delete("/api/user/wrong")
    response.status_code.should.equal(404)


@web_test
def test_api_delete_user_valid_email(context):
    ("DELETE on /api/user/<email> with valid email ")
    user = User.create_user('ramadan2', 'ramadan@thebest.com', 'pass12344')
    response = context.http.delete("/api/user/{}".format(user.email))
    response.status_code.should.equal(200)
    data = json.loads(response.data)
    data.should.have.key("first_name").being.equal(user.first_name)
    data.should.have.key("email").being.equal(user.email)
    data.should.have.key("uuid").being.equal(
        user.uuid
    )
    User.query.filter_by(email='ramadan@thebest.com').first().should.equal(None)