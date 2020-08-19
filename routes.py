from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    get_jwt_identity, verify_jwt_in_request, jwt_refresh_token_required
)

from sqlalchemy.exc import IntegrityError

from app import db
from models import User


user_blueprint = Blueprint('user', __name__, url_prefix='/user')


@user_blueprint.route('', methods=['POST'], strict_slashes=False)
def insert_user():
    errors = []

    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    if not username:
        errors.append('Invalid username!')
    if not email:
        errors.append('Invalid email!')
    if not password or len(password) < 5:
        errors.append('Invalid password!')

    if errors:
        return jsonify({
            'error': errors,
        }), 400

    try:
        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        return jsonify({
            'error': 'User already exists',
        }), 400

    return jsonify({
        'message': 'OK'
    }), 201


@user_blueprint.route('/auth', methods=['POST'], strict_slashes=False)
def auth():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.authenticate(username, password)
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity={
        username: user.username
    })
    refresh_token = create_refresh_token(identity={
        username: user.username
    })

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token
    })


@user_blueprint.route('/refresh', methods=['POST'], strict_slashes=False)
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    return jsonify({
        'access_token': access_token,
    })


@user_blueprint.route('/validate', methods=['GET'])
def validate():
    verify_jwt_in_request()
    return jsonify(), 200
