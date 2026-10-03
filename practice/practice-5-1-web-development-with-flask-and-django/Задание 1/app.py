"""
A simple Flask-based advertisement management API.

This application stores ads in a local JSON file (`storage.json`)
and supports full CRUD operations (Create, Read, Update, Delete).
Each ad contains an ID, title, description, owner, and creation timestamp.

Routes:
    POST   /api/v1/ads          — Create a new advertisement.
    GET    /api/v1/ads/<id>     — Retrieve a specific advertisement.
    GET    /api/v1/ads          — Retrieve all advertisements.
    PUT    /api/v1/ads/<id>     — Update an existing advertisement.
    DELETE /api/v1/ads/<id>     — Remove an advertisement.
"""

from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# Init Storage
STORAGE_FILE = 'storage.json'


def load_storage():
    """
    Load the advertisement storage from disk.

    Returns:
        tuple(dict, int):
            - items (dict): A dictionary mapping ad IDs to advertisement objects.
            - next_id (int): The next available ID for new advertisements.

    If the storage file does not exist, returns an empty storage and ID = 0.
    """
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, 'r') as f:
            data = json.load(f)
            return data.get('items', {}), data.get('next_id', 0)
    return {}, 0


def save_storage(items, next_id):
    """
    Save the advertisement storage to disk.

    Args:
        items (dict): The dictionary of stored advertisements.
        next_id (int): The next available advertisement ID.

    Writes data to the JSON storage file.
    """
    with open(STORAGE_FILE, 'w') as f:
        json.dump({'items': items, 'next_id': next_id}, f)


storage, next_id = load_storage()

# Init Const Variables
ID_NAME = 'id'
TITLE_NAME = 'title'
DESCRIPTION_NAME = 'description'
OWNER_NAME = 'owner'
CREATED_AT_NAME = 'created_at'

API_ROUTE = '/api/v1/ads'


# Routes
@app.route(API_ROUTE, methods=['POST'])
def create_ad():
    """
    Create a new advertisement.

    Expects JSON containing fields:
        - title (str)
        - description (str)
        - owner (str)

    Returns:
        Response: JSON representation of the created advertisement
                  along with HTTP 201 status code.
    """
    global next_id
    data = request.get_json()

    ad = {
        ID_NAME: next_id,
        TITLE_NAME: data[TITLE_NAME],
        DESCRIPTION_NAME: data[DESCRIPTION_NAME],
        CREATED_AT_NAME: datetime.now().isoformat(),
        OWNER_NAME: data[OWNER_NAME]
    }

    storage[str(next_id)] = ad
    next_id += 1
    save_storage(storage, next_id)

    return jsonify(ad), 201


@app.route(API_ROUTE + '/<int:id>', methods=['GET'])
def get_ad(id: int):
    """
    Retrieve an advertisement by ID.

    Args:
        id (int): The ID of the advertisement.

    Returns:
        Response: JSON representation of the advertisement,
                  or an error message if not found.
    """
    if str(id) not in storage:
        return jsonify({'error': 'Ad not found'}), 404
    return jsonify(storage[str(id)])


@app.route(API_ROUTE, methods=['GET'])
def list_ads():
    """
    Retrieve all stored advertisements.

    Returns:
        Response: JSON dictionary containing all advertisements.
    """
    return jsonify(storage)


@app.route(API_ROUTE + '/<int:id>', methods=['PUT'])
def update_ad(id: int):
    """
    Update an existing advertisement.

    Args:
        id (int): The ID of the advertisement to update.

    Expects JSON with any subset of:
        - title (str)
        - description (str)
        - owner (str)

    Returns:
        Response: JSON representation of the updated advertisement,
                  or 404 if the ad does not exist.
    """
    if str(id) not in storage:
        return jsonify({'error': 'Ad not found'}), 404

    data = request.get_json()
    ad = storage[str(id)]

    ad[TITLE_NAME] = data.get(TITLE_NAME, ad[TITLE_NAME])
    ad[DESCRIPTION_NAME] = data.get(DESCRIPTION_NAME, ad[DESCRIPTION_NAME])
    ad[OWNER_NAME] = data.get(OWNER_NAME, ad[OWNER_NAME])

    save_storage(storage, next_id)
    return jsonify(ad)


@app.route(API_ROUTE + '/<int:id>', methods=['DELETE'])
def delete_ad(id: int):
    """
    Delete an advertisement by ID.

    Args:
        id (int): The ID of the advertisement to delete.

    Returns:
        Response: Empty response with HTTP 204 status code,
                  or an error if the ad does not exist.
    """
    if str(id) not in storage:
        return jsonify({'error': 'Ad not found'}), 404

    del storage[str(id)]
    save_storage(storage, next_id)
    return '', 204


# Start App
if __name__ == '__main__':
    app.run(debug=True)
