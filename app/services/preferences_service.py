import json
import os.path
from pydantic import BaseModel,Field
from services.book_service import BookService

from db.db import get_session


class UserPreferences(BaseModel):
    books: list[str] = Field(default_factory=list) #stores ids
    authors:list[str] = Field(default_factory=list) #stores ids
    categories:list[str] = Field(default_factory=list) #stores categories names

class PreferencesService:
    def __init__(self,username):
        self.username = username
        self.file_path = os.path.join(os.getcwd(),'data','user_preferences',f"{self.username}_preferences.json")
        self.preferences = UserPreferences()
        self.books_service : BookService = BookService(get_session())
        self.load_preferences()

    def load_preferences(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r") as file:
                    data = json.load(file)
                    self.preferences = UserPreferences(**data)
            else:
                self.save_preferences()
        except Exception as e:
            raise Exception(f"Error loading preferences for user '{self.username}': {e}")

    def save_preferences(self):
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, "w") as file:
                json.dump(self.preferences.model_dump(), file, indent=4)
        except Exception as e:
            raise Exception(f"Error saving preferences for user '{self.username}': {e}")

    def get_preferences(self):
        return self.preferences

    def add_book(self,book_id):
        if book_id not in self.preferences.books:
            self.preferences.books.append(book_id)
            self.save_preferences()

    def add_books(self, book_ids):
        added_books = [book_id for book_id in book_ids if book_id not in self.preferences.books]
        self.preferences.books.extend(added_books)
        self.save_preferences()

    def add_author(self, author_id):
        if author_id not in self.preferences.authors:
            self.preferences.authors.append(author_id)
            self.save_preferences()

    def add_authors(self, author_ids):
        added_authors = [author_id for author_id in author_ids if author_id not in self.preferences.authors]
        self.preferences.authors.extend(added_authors)
        self.save_preferences()

    def add_category(self, category_name):
        if category_name not in self.preferences.categories:
            self.preferences.categories.append(category_name)
            self.save_preferences()

    def add_categories(self, category_names):
        added_categories = [category_name for category_name in category_names if
                            category_name not in self.preferences.categories]
        self.preferences.categories.extend(added_categories)
        self.save_preferences()

    def remove_book(self, book_id):
        if book_id in self.preferences.books:
            self.preferences.books.remove(book_id)
            self.save_preferences()

    def remove_author(self, author_id):
        if author_id in self.preferences.authors:
            self.preferences.authors.remove(author_id)
            self.save_preferences()

    def remove_category(self, category_name):
        if category_name in self.preferences.categories:
            self.preferences.categories.remove(category_name)
            self.save_preferences()


    def get_books_data(self):
        return [self.books_service.find_by_id(book_id).to_dict() for book_id in self.preferences.books]

    def get_authors_data(self):
        return [self.book_service.find_author_by_id(author_id).to_dict() for author_id in self.preferences.authors]

    def get_categories_data(self):
        return self.preferences.categories

    def get_all_data(self):
        return {
            "books": self.get_books_data(),
            "authors":self.get_authors_data(),
            "categories":self.get_categories_data()
        }
