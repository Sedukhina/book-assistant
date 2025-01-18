from flask import Blueprint, session, request, jsonify

from services.preferences_service import PreferencesService

preferences_api = Blueprint('preferences', __name__, url_prefix='/preferences')

@preferences_api.route('/', methods=['GET'])
def get_preferences():
    username = session.get('username')
    if not username:
        return jsonify({"error": "Unauthorized"}), 401
    service = PreferencesService(username)
    return jsonify(service.get_preferences().dict())

@preferences_api.route('/<option>', methods=['GET'])
def get_preferences_by_option(option):
    username = session.get('username')
    if not username:
        return jsonify({"error": "Unauthorized"}), 401
    service = PreferencesService(username)
    try:
        return jsonify(service.get_preferences_by_option(option))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@preferences_api.route('/book', methods=['POST'])
def add_book():
    username = session.get('username')
    if not username:
        return jsonify({"error": "Unauthorized"}), 401
    book_id = request.json.get('book_id')
    if not book_id:
        return jsonify({"error": "book_id is required"}), 400
    service = PreferencesService(username)
    service.add_book(book_id)
    return jsonify({"message": "Book added"})

@preferences_api.route('/books', methods=['POST'])
def add_books():
    username = session.get('username')
    if not username:
        return jsonify({"error": "Unauthorized"}), 401
    book_ids = request.json.get('book_ids')
    if not book_ids or not isinstance(book_ids, list):
        return jsonify({"error": "book_ids must be a list"}), 400
    service = PreferencesService(username)
    service.add_books(book_ids)
    return jsonify({"message": "Books added"})

@preferences_api.route('/book', methods=['DELETE'])
def remove_book():
    username = session.get('username')
    if not username:
        return jsonify({"error": "Unauthorized"}), 401
    book_id = request.json.get('book_id')
    if not book_id:
        return jsonify({"error": "book_id is required"}), 400
    service = PreferencesService(username)
    service.remove_book(book_id)
    return jsonify({"message": "Book removed"})

@preferences_api.route('/author', methods=['POST'])
def add_author():
    username = session.get('username')
    if not username:
        return jsonify({"error": "Unauthorized"}), 401
    author_id = request.json.get('author_id')
    if not author_id:
        return jsonify({"error": "author_id is required"}), 400
    service = PreferencesService(username)
    service.add_author(author_id)
    return jsonify({"message": "Author added"})

@preferences_api.route('/authors', methods=['POST'])
def add_authors():
    username = session.get('username')
    if not username:
        return jsonify({"error": "Unauthorized"}), 401
    author_ids = request.json.get('author_ids')
    if not author_ids or not isinstance(author_ids, list):
        return jsonify({"error": "author_ids must be a list"}), 400
    service = PreferencesService(username)
    service.add_authors(author_ids)
    return jsonify({"message": "Authors added"})

@preferences_api.route('/author', methods=['DELETE'])
def remove_author():
    username = session.get('username')
    if not username:
        return jsonify({"error": "Unauthorized"}), 401
    author_id = request.json.get('author_id')
    if not author_id:
        return jsonify({"error": "author_id is required"}), 400
    service = PreferencesService(username)
    service.remove_author(author_id)
    return jsonify({"message": "Author removed"})

@preferences_api.route('/category', methods=['POST'])
def add_category():
    username = session.get('username')
    if not username:
        return jsonify({"error": "Unauthorized"}), 401
    category_name = request.json.get('category_name')
    if not category_name:
        return jsonify({"error": "category_name is required"}), 400
    service = PreferencesService(username)
    service.add_category(category_name)
    return jsonify({"message": "Category added"})

@preferences_api.route('/categories', methods=['POST'])
def add_categories():
    username = session.get('username')
    if not username:
        return jsonify({"error": "Unauthorized"}), 401
    category_names = request.json.get('category_names')
    if not category_names or not isinstance(category_names, list):
        return jsonify({"error": "category_names must be a list"}), 400
    service = PreferencesService(username)
    service.add_categories(category_names)
    return jsonify({"message": "Categories added"})

@preferences_api.route('/category', methods=['DELETE'])
def remove_category():
    username = session.get('username')
    if not username:
        return jsonify({"error": "Unauthorized"}), 401
    category_name = request.json.get('category_name')
    if not category_name:
        return jsonify({"error": "category_name is required"}), 400
    service = PreferencesService(username)
    service.remove_category(category_name)
    return jsonify({"message": "Category removed"})

