from flask import Blueprint, render_template, request, jsonify
from services.book_service import BookService

from db.db import get_session
from sqlalchemy.orm import defer

books_bp = Blueprint('books',__name__,url_prefix='/books')

#get global session
session = get_session()

# Creates Book service
book_service = BookService(session)


@books_bp.route('/',methods=['GET'])
def books():
    """
        Render book template
    """
    return render_template('books.html')


#TODO create book template
# TODO fetch book details from api
@books_bp.route('/<book_id>')
def book_details(book_id):

    book = book_service.find_by_id(book_id)
    print(book)
    return render_template('book.html', book=book)