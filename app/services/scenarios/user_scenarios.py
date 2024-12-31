from db.db import get_session
from services.book_service import BookService
from services.user_service import UserService

session = get_session()
book_service = BookService(session)
user_service = UserService(book_service)


def favourite_books():
        books_ids = user_service.get_preferences("books")
        books = []
        for book_id in books_ids:
            try:
                book = book_service.find_book_by_id(book_id)
                if book:
                    books.append({"title":book.title,'categories':book.category,"author":book.author.name})
            except Exception as e:
                print('ooops')

        if not books:
            return 'Oops, there is no saved books'
        message = 'Your favourite list:\n'
        for book in books:
            message+=(f"Book:\n"
                      f"Title:{book['title']}\n"
                      f"Categories:{book['category']}\n"
                      f"Author {book['author']}\n")

def favourite_authors():
    authors_ids = user_service.get_preferences("authors")
    authors = []
    for author_id in authors_ids:
        try:
            author = book_service.find_author_by_id(author_id)
            if author:
                authors.append({"name":author.name})
        except Exception as e:
            print('oops')

    if not authors:return "There is no saved authors"
    message = "Your favourite authors:\n"

    for author in authors: message+= f"{author['name']}\n"

    return message

def favourite_categories():
    categories = user_service.get_preferences('categories')
    if not categories: return "There is no saved categories"

    message = "Your favourite categories\n"

    for category in categories: message+=f"{category}\n"

    return message

def add_book_to_favourite(title):
    try:
        if not title: return "No title"

        user_service.add_book_to_favourite(title)
        return "Book added to favourite"
    except Exception as e:
        return f"{e}"


def remove_book_from_favourite(title):
    try:
        if not title: return "No title"

        user_service.remove_book_from_favourite(title)
        return "Book removed from favourite"
    except Exception as e:
        return f"{e}"

def add_author_to_favourite(name):
    try:
        if not name: return "No Author name"

        user_service.add_author_to_favourite(name)
        return "Book added to favourite"
    except Exception as e:
        return f"{e}"

def remove_author_from_favourite(name):
    try:
        if not name: return "No Author name"

        user_service.remove_author_from_favourite(name)
        return "Author removed from favourite"
    except Exception as e:
        return f"{e}"

def add_category_to_favourite(name):
    try:
        if not name: return "No Category name"

        user_service.add_category_to_favourite(name)
        return "Category added to favourite"
    except Exception as e:
        return f"{e}"

def remove_category_from_favourite(name):
    try:
        if not name: return "No Category name"

        user_service.remove_category_from_favourite(name)
        return "Author removed from favourite"
    except Exception as e:
        return f"{e}"

def get_commands():
    return {
        ('нагадай мені улюблені книги','remind me of my favorite books'):favourite_books,
        ('нагадай мені улюблені жанри','remind me of my favorite categories'):favourite_categories,
        ('нагадай мені улюблених письменників','remind me of my favorite writers'):favourite_authors,
        ('додай книгу до улюблених','add book to favourite'):add_book_to_favourite,
        ('додай автора до улюблених', 'add author to favourite'): add_author_to_favourite,
        ('додай категорію до улюблених', 'add category to favourite'): add_category_to_favourite,
        ('видали книгу з улюблених','remove book from favourite'):remove_book_from_favourite,
        ('видали автора з улюблених', 'remove author from favourite'): remove_book_from_favourite,
        ('видали категорію з улюблених', 'remove category from favourite'): remove_category_from_favourite,
    }
