from flask import Blueprint, jsonify

from ..extensions import db
from ..models import Post

api = Blueprint('api', __name__)


@api.route('/<post_name>')
def create_post(post_name):
    return {231:post_name}

@api.route('/users', methods=['GET'])
def get_users():
    # Fetch user data (database, external API, etc.)
    users = [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]
    return jsonify(users)