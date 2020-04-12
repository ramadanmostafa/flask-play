#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from flask import render_template, Blueprint, request

from app.application.models import User
from .utils import json_response, get_md5
from .validators import validate_email_format, validate_email_already_exists, validate_field_required, run_validators

app_bp = Blueprint('application', __name__)


@app_bp.route("/", methods=["GET"])
def frontend():
    return render_template("index.html")


def my_backend_function():
    payload = {"hello": "world"}
    return payload


@app_bp.route("/api/example", methods=["GET"])
def api_example_route_get():
    payload = my_backend_function()
    return json_response(payload, 200)


@app_bp.route("/api/calculate-md5", methods=["POST"])
def api_calculate_md5():
    request_data = request.get_json() or {}
    data = request_data.get('data')
    errors = run_validators([{'field_name': 'data', 'func': validate_field_required, 'field_val': data}])
    if errors:
        return json_response(errors, 400)
    return json_response({'md5': get_md5(data=data)}, 200)


@app_bp.route("/api/user", methods=["POST"])
def api_create_user():
    request_data = request.get_json() or {}
    first_name = request_data.get('first_name')
    email = request_data.get('email', '')
    password = request_data.get('password')
    validators = [
        {'field_name': 'first_name', 'func': validate_field_required, 'field_val': first_name},
        {'field_name': 'email', 'func': validate_field_required, 'field_val': email},
        {'field_name': 'password', 'func': validate_field_required, 'field_val': password},
        {'field_name': 'email', 'func': validate_email_format, 'field_val': email},
        {'field_name': 'email', 'func': validate_email_already_exists, 'field_val': email},
    ]
    errors = run_validators(validators)
    if errors:
        return json_response(errors, 400)
    user = User.create_user(first_name, email, password)
    return json_response(user.to_dict(), 200)


@app_bp.route("/api/user/<uuid>", methods=["GET", "PUT"])
def api_user_details(uuid):
    user = User.query.filter_by(uuid=uuid).first()
    if not user:
        return json_response({}, 404)
    if request.method == 'GET':
        return json_response(user.to_dict(), 200)
    # update user data
    request_data = request.get_json() or {}
    first_name = request_data.get('first_name')
    email = request_data.get('email', '')
    password = request_data.get('password')
    if email:
        validators = [
            {'field_name': 'email', 'func': validate_email_format, 'field_val': email},
            {'field_name': 'email', 'func': validate_email_already_exists, 'field_val': email},
        ]
        errors = run_validators(validators)
        if errors:
            return json_response(errors, 400)
    user.update_user(first_name, email, password)
    return json_response(user.to_dict(), 200)


@app_bp.route("/api/users", methods=["GET"])
def api_list_users():
    data = []
    for user in User.query.all():
        data.append(user.to_dict())
    return json_response(data, 200)


@app_bp.route("/api/user/<email>", methods=["DELETE"])
def api_user_delete_by_email(email):
    is_deleted, data = User.delete_by_email(email)
    if not is_deleted:
        return json_response({}, 404)
    return json_response(data, 200)
