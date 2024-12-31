from flask import Blueprint, request, jsonify
from services.book_service import BookService

from db.db import get_session

#get global session
session = get_session()

# Creates Book service
books_service = BookService(session)


authors_api = Blueprint('authors_api',__name__,url_prefix='/authors')

@authors_api.route('/names',methods=['GET'])
def get_names():
    try:
        authors = book_service.get_authors_names()
        return jsonify([{"id": author.author_id, "name": author.name} for author in authors])
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@authors_api.route('/author',methods=['GET'])
def find_by_name():
    try:
        name = request.args.get("name")
        author = books_service.find_author(name)
        if not author:
            return "Author not found",404

        # Retrieve the author's books
        books = [{"id": book.id, "title": book.title} for book in author.books]

        # Return the author details with their books
        return jsonify({
            "id": author.author_id,
            "name": author.name,
            "books": books
        }), 200
    except Exception as e:
        return f"{e}",500
