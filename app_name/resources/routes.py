"""
Routes for this resource group module
"""

from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from .models import ResourceA

from app_name import app

from app_name.database import db

from app_name.users.models import User

from app_name.util import status, responses
from app_name.util.exceptions import protect_500


@app.route('/resource-a', methods=['POST'])
@protect_500
@jwt_required
def create_resource_a():
    """
    Creates a resource A
    :return:
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return responses.user_not_found()

    data = request.get_json()
    resource_a = ResourceA(**data)
    resource_a.owner_id = user_id

    user.resource_a_set.append(resource_a)

    db.session.add(resource_a)
    db.session.commit()

    return responses.resource_created(ResourceA.__name__)


@app.route('/resource-a', methods=['GET'])
@protect_500
def get_all_resource_a():
    """
    Returns all resource A's
    :return:
    """
    resource_a_set = ResourceA.query.all()

    return jsonify({
        'items': [resource_a.to_dict() for resource_a in resource_a_set]
    }), status.OK


@app.route('/resource-a/<resource_a_id>', methods=['GET'])
@protect_500
def get_resource_a(resource_a_id):
    """
    Returns resource's information
    :return:
    """
    resource_a = ResourceA.query.get(resource_a_id)

    if not resource_a:
        return responses.resource_not_found(ResourceA.__name__)

    return jsonify(resource_a.to_dict()), status.OK


@app.route('/resource-a/<resource_a_id>', methods=['PUT'])
@protect_500
@jwt_required
def update_resource_a(resource_a_id):
    """
    Updates resource A details
    :return:
    """
    resource_a = ResourceA.query.get(resource_a_id)

    if not resource_a:
        return responses.resource_not_found(ResourceA.__name__)

    user_id = get_jwt_identity()

    if user_id != resource_a.owner_id:
        return responses.unauthorized()

    valid_attrs = {'name'}

    update_attrs = request.get_json()

    if not update_attrs:
        return responses.missing_params()

    if not all(attr in valid_attrs for attr in update_attrs):
        return responses.invalid_request_keys(set(update_attrs) - valid_attrs)

    for attr, value in update_attrs.items():
        setattr(resource_a, attr, value)

    db.session.commit()

    return responses.resource_updated(ResourceA.__name__)


@app.route('/resource-a/<resource_a_id>', methods=['DELETE'])
@protect_500
@jwt_required
def delete_resource_a(resource_a_id):
    """
    Deletes resource A
    :return:
    """
    resource_a = ResourceA.query.get(resource_a_id)

    if not resource_a:
        return responses.resource_not_found(ResourceA.__name__)

    user_id = get_jwt_identity()

    if user_id != resource_a.owner_id:
        return responses.unauthorized()

    db.session.delete(resource_a)
    db.session.commit()

    return responses.resource_deleted(ResourceA.__name__)
