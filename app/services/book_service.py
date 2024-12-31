from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from db.db_models import BookBase, AuthorBase
from typing_extensions import reveal_type

#TODO add error handling

class BookService:
    def __init__(self,session:Session):
        self.session = session

    def find_by_id(self,book_id):
        """
        Return book by id
        """
        try:
            return self.session.query(BookBase).filter(BookBase.id == book_id).first()
        except SQLAlchemyError as e:
            print(f"{e}")

    def find_by_title(self,title):
        """
        Return all books with param in title
        """
        try:
            return  self.session.query(BookBase).filter(BookBase.title.ilike(f"%{title}%")).all()
        except SQLAlchemyError as e:
            print(f"{e}")

    def find_one_by_title(self,title):
        """
        Return single book by title
        """
        try:
            return  self.session.query(BookBase).filter(BookBase.title.ilike(f"%{title}%")).first()
        except SQLAlchemyError as e:
            print(f"{e}")

    def find_all(self):
        """
         Returns all authors
        """
        try:
            return self.session.query(BookBase).all()
        except SQLAlchemyError as e:
            print(f"{e}")

    def find_author_by_id(self,author_id):
        try:
            return self.session.query(AuthorBase).filter(AuthorBase.author_id == author_id).first()
        except SQLAlchemyError as e:
            print(f"{e}")

    def find_author(self,name):
        """
        Return author by name
        """
        try:
            return self.session.query(AuthorBase).filter(AuthorBase.name.ilike(f"%{name}%")).first()
        except SQLAlchemyError as e:
            print(f"{e}")

    def find_all_authors(self):
        """
            Returns all authors
        """
        try:
            return self.session.query(AuthorBase).all()
        except SQLAlchemyError as e:
            print(f"{e}")

    def find_books_by_author_name(self,author_name):
        """
            Returns author's books
        """
        try:
            return (
                self.session.query(BookBase)
                .join(AuthorBase, BookBase.author_id == AuthorBase.id)
                .filter(AuthorBase.name.ilike(f"%{author_name}%"))
                .all()
            )
        except SQLAlchemyError as e:
            print(f"{e}")

    def find_books_by_author(self, author_id):
        """
        Finds all books written by a specific author using `author_id`.
        """
        try:
            return (
                self.session.query(BookBase)
                .filter(BookBase.author_id == author_id)
                .all()
            )
        except SQLAlchemyError as e:
            print(f"{e}")

    def get_filtered_books(self, **filters):
        """
            Filters books by params title, categories, author's name, publish range
        """
        try:
            query = self.session.query(BookBase).join(AuthorBase)

            if filters.get('title'): # Filter by title
                query = query.filter(BookBase.title.ilike(f"%{filters['title']}%"))

            if filters.get('categories'):# Filter by categories
                query = query.filter(BookBase.category.in_(filters['categories']))


            if filters.get('author'): # Filter by author
                query = query.filter(AuthorBase.name.ilike(f"%{filters['author']}%"))

            # Filter by published year range
            if filters.get('published_year_from'):
                query = query.filter(BookBase.published_date >= f"{filters['published_year_from']}-01-01")
            if filters.get('published_year_to'):
                query = query.filter(BookBase.published_date <= f"{filters['published_year_to']}-12-31")

            return query.all()
        except SQLAlchemyError as e:
            print(f"error {e}")
            raise

    def get_book_previews(self):
        """
            Returns books previews ( id, title, author_name)
        """
        try:
            results = (
                self.session.query(BookBase.id, BookBase.title, AuthorBase.name.label("author_name"))
                .join(AuthorBase, BookBase.author_id == AuthorBase.author_id)
                .all()
            )
            return results
        except SQLAlchemyError as e:
            print(f"{e}")

    def get_books_titles(self):
        """
            Returns simplified books previews (id, title)
        """
        try:
            return self.session.query(BookBase.id,BookBase.title).all()
        except SQLAlchemyError as e:
            print(f"{e}")

    def get_authors_names(self):
        """
            Returns simplified authors previews (id, name)
        """
        try:
            return self.session.query(AuthorBase.author_id,AuthorBase.name).all()
        except SQLAlchemyError as e:
            print(f"{e}")