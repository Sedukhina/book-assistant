from flask import Blueprint, request, jsonify, session
from services.book_service import BookService
from services.preferences_service import PreferencesService

from db.db import get_session

#get global session
global_session = get_session()

# Creates Book service
book_service = BookService(global_session)


books_api = Blueprint('books_api',__name__,url_prefix='/books')


@books_api.route('/', methods=['GET'])
def get_books():
    """
        Api call to get boooks by filters
    """
    try:
        username = session.get('username')
        if not username:
            return jsonify({"error": "Unauthorized"}), 401

        preferences_service = PreferencesService(username)

        title = request.args.get("title", "").strip().lower()
        categories = request.args.get("genre", "").strip().lower() #TODO: categories should be separated in database
        author = request.args.get("author", "").strip().lower()
        published_year_from = request.args.get("year_from")
        published_year_to = request.args.get("year_to")

        filters = {
            'title': title,
            'categories': categories.split(',') if categories else [],
            'author': author,
            'published_year_from': published_year_from,
            'published_year_to': published_year_to
        }

        #retrives books from  db
        filtered = book_service.get_filtered_books(**filters)

        user_preferences = preferences_service.get_preferences()

        # add liked filed to books

        for book in filtered:
            book["liked"] = book["id"] in user_preferences.books

        #convert it to json-readable format
        # filtered_books = [book for book in filtered]

        return jsonify(filtered)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@books_api.route('/book',methods=['GET'])
def book_details():
    """
        Api call to get book by id
    """
    try:
        book_id = request.args.get("book_id", "").strip()

        book = book_service.find_by_id(book_id)

        if book is None:
            return jsonify({"error": "Book doesn't exist"}), 404

        return jsonify(book)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@books_api.route('/titles',methods=['GET'])
def get_titles():
    try:
        books_titles = book_service.get_books_titles()
        return jsonify([{"id": book.id, "title": book.title} for book in books_titles])
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500