
from db.db import get_session
from services.book_service import BookService

session = get_session()
book_service = BookService(session)

def book_details(title):
    try:
        data = book_service.find_one_by_title(title)
        if data is None:
            return 'Нажаль, книги з такою назвою не існує'

        book = data.to_preview()

        return (f"Книга {book['title']}\n"
                f"написана {book['author']}.\n"
                f"Жанри: {', '.join(book['categories'])}.\n"
                f"Опублікована у {book['publishDate']}.\n")
    except Exception as e:
        print(f"error on command :{e}")
        return 'Something went wrong'

def author_books(author):
    try:
        books = book_service.find_books_by_author_name(author)
        print(books)
        return f"Author books {books}" #TODO make beautiful
    except Exception as e:
        print(f"error on command :{e}")
        return 'Something went wrong'

def get_commands():
    return {
        ('надай інформацію про книгу','tell me about the book'): book_details,
        ('які книги написав', 'what books have'): author_books
    }

