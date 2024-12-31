from flask import Blueprint, jsonify, request
from db.db import get_session
from services.user_service import UserService
from services.book_service import BookService

session = get_session()
book_service = BookService(get_session())
user_service = UserService(book_service)


user_api = Blueprint('user',__name__,url_prefix='/user')

@user_api.route('/preferences', methods=['GET'])
def get_user_preferences():
    """
    Returns all user preferences
    """
    try:
        preferences = user_service.get_preferences()

        type = request.args.get('type')

        if type is None:
            return jsonify({
                'preferences': preferences}), 200
        elif type in preferences:
            return jsonify({f"{type}":preferences.get(type)}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#TODO fix, separate to api calls



@user_api.route('/preferences/<preference_type>', methods=['GET', 'POST', 'DELETE'])
def preferences(preference_type):
    """
    Handle user preferences for books, authors, and categories.
    """
    try:
        # Map preference types to their respective add/remove methods
        valid_types = {
            "books": {
                "add": user_service.add_books_to_favourite,
                "remove": user_service.remove_books_from_favourite
            },
            "authors": {
                "add": user_service.add_authors_to_favourite,
                "remove": user_service.remove_authors_from_favourite
            },
            "categories": {
                "add": user_service.add_categories_to_favourite,
                "remove": user_service.remove_categories_from_favourite
            }
        }

        # Validate preference type
        if preference_type not in valid_types:
            return jsonify({"error": f"Invalid preference type: '{preference_type}'. Allowed types: {', '.join(valid_types.keys())}"}), 400

        if request.method == 'GET':
            # Return the user's preferences for the given type
            preferences = user_service.get_preferences(preference_type)
            return jsonify({"message": f"Favorite {preference_type} retrieved successfully", preference_type: preferences}), 200

        elif request.method in {'POST', 'DELETE'}:
            # Ensure the request is JSON
            if not request.is_json:
                return jsonify({"error": "Invalid request format. JSON expected."}), 400

            # Extract the data from the request
            data = request.json.get(preference_type)
            if not data:
                return jsonify({"error": f"Missing '{preference_type}' field in request payload."}), 400

            # Call the appropriate add or remove method
            action = "add" if request.method == 'POST' else "remove"
            result = valid_types[preference_type][action](data)
            return jsonify({"message": result}), 200

    except Exception as e:
        print(f"Error in preferences handler: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500


@user_api.route('/preferences/<preference_type>/single', methods=['GET', 'POST', 'DELETE'])
def single(preference_type):
    """
    Handle user preferences for books, authors, and categories.
    """
    try:
        # Map preference types to their respective add/remove methods
        valid_types = {
            "books": {
                "add": user_service.add_book_to_favourite,
                "remove": user_service.remove_book_from_favourite,
                'key': 'book'
            },
            "authors": {
                "add": user_service.add_author_to_favourite,
                "remove": user_service.remove_author_from_favourite,
                "key": 'author'
            },
            "categories": {
                "add": user_service.add_category_to_favourite,
                "remove": user_service.remove_category_from_favourite,
                "key": "category"
            }
        }

        # Validate preference type
        if preference_type not in valid_types:
            return jsonify({"error": f"Invalid preference type: '{preference_type}'. Allowed types: {', '.join(valid_types.keys())}"}), 400

        if request.method == 'GET': #TODO remove, or change to get full object details
            # Return the user's preferences for the given type
            preferences = user_service.get_preferences(preference_type)
            return jsonify({"message": f"Favorite {preference_type} retrieved successfully", preference_type: preferences}), 200

        elif request.method in {'POST', 'DELETE'}:
            # Ensure the request is JSON
            if not request.is_json:
                return jsonify({"error": "Invalid request format. JSON expected."}), 400

            # Extract the data from the request
            data = request.json.get(valid_types[preference_type]['key'])
            if not data:
                return jsonify({"error": f"Missing '{preference_type}' field in request payload."}), 400

            # Call the appropriate add or remove method
            action = "add" if request.method == 'POST' else "remove"
            result = valid_types[preference_type][action](data)
            return jsonify({"message": result}), 200

    except Exception as e:
        print(f"Error in preferences handler: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500


@user_api.route('/preferences/<preference_type>/id', methods=['GET', 'POST', 'DELETE'])
def by_id(preference_type):
    """
    Handle user preferences for books, authors, and categories.
    """
    try:
        # Map preference types to their respective add/remove methods
        valid_types = {
            "books": {
                "add": user_service.add_book_id_to_favourite,
                "remove": user_service.remove_book_id_from_favourite,
                'key': 'book_id'
            },
            "authors": {
                "add": user_service.add_author_id_to_favourite,
                "remove": user_service.remove_author_id_from_favourite,
                "key": 'author_id'
            },
            "categories": {
                "add": user_service.add_category_to_favourite,
                "remove": user_service.remove_category_from_favourite,
                "key": "category"
            }
        }

        # Validate preference type
        if preference_type not in valid_types:
            return jsonify({"error": f"Invalid preference type: '{preference_type}'. Allowed types: {', '.join(valid_types.keys())}"}), 400

        if request.method == 'GET': #TODO remove
            # Return the user's preferences for the given type
            preferences = user_service.get_preferences(preference_type)
            return jsonify({"message": f"Favorite {preference_type} retrieved successfully", preference_type: preferences}), 200

        elif request.method in {'POST', 'DELETE'}:
            # Ensure the request is JSON
            if not request.is_json:
                return jsonify({"error": "Invalid request format. JSON expected."}), 400

            # Extract the data from the request
            data = request.json.get(valid_types[preference_type]['key'])
            if not data:
                return jsonify({"error": f"Missing '{preference_type}' field in request payload."}), 400

            # Call the appropriate add or remove method
            action = "add" if request.method == 'POST' else "remove"
            result = valid_types[preference_type][action](data)
            return jsonify({"message": result}), 200

    except Exception as e:
        print(f"Error in preferences handler: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500