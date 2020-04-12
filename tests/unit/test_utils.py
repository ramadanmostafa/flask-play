from flask import Response
from app.application.utils import json_response, get_md5


def test_json_response_returns_flask_response():
    ("json_response() should set the proper header and serialize the data as json")

    # Given a dictionary with data
    data = {"foo": "bar"}

    # When I call json_response
    response = json_response(data)

    # Then it should have returned a flask response object
    response.should.be.a(Response)

    # And the headers should have a content-type
    response.headers.should.have.key("Content-Type")

    # And it should be application/json
    response.headers["Content-Type"].should.equal("application/json")

    # And the data should be serialized as json
    response.data.should.equal(b'{\n  "foo": "bar"\n}')


def test_get_md5():
    get_md5('test').should.equal('098f6bcd4621d373cade4e832627b4f6')
