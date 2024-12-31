from flask import session
from sqlalchemy.exc import SQLAlchemyError
from services.book_service import BookService

#TODO add error handling, maybe clear code
class UserService:
    def __init__(self,book_service:BookService):
        self.book_service = book_service

    def get_preferences(self,preference_type=None):
        if 'preferences' not in session:
            session['preferences'] = {
                'books': [],  # stores book ids
                'categories': [],  # stores category names
                'authors': []  # stores author ids
            }

        if preference_type:
            return session['preferences'][preference_type]

        return session['preferences']

    def is_value_in_list(self,value,preference_type):
        try:
            # Get the preferences list for the specified type
            preferences = self.get_preferences(preference_type)

            # Check if the value exists in the list
            return value in preferences
        except KeyError:
            print(f"Invalid preference type: {preference_type}")
            return False
        except Exception as e:
            print(f"Error in is_value_in_list: {e}")
            return False

    # modifies preferences session
    def modify_preferences(self,data, param, action_type):
        print(f"data:{data},param: {param},action:{action_type},islist:{isinstance(data,list)}")

        # check is correct data
        if not isinstance(data, list):
            raise Exception({'error': 'Invalid data format, expected a list'})
            # retrive preference session object
        preferences = self.get_preferences()
        print(f"before {param} :{preferences[param]}")

        # set action
        if action_type == 'add':
            print(f'hello from add, {preferences}, {param in preferences}')
            preferences[param] = list(set(preferences[param]) | set(data))
        elif action_type == 'remove':
            preferences[param] = list(set(preferences[param]) - set(data))
        else:
            raise Exception({'error': 'Unknown command'})

        session.modified = True
        print(f"success ({param}) :{preferences[param]}")

        return preferences[param]


    def add_to_favourite(self, value, preference_type):
        try:
            data = self._find_value(preference_type,value)

            if self.is_value_in_list(data,preference_type):
                raise Exception( f"{value} already in favourite list")

            self.modify_preferences([data], preference_type, 'add')
            return 'Ok'
        except SQLAlchemyError:
            raise 'Something went wrong'

    def remove_from_favourite(self, value, preference_type):
        try:
            data = self._find_value(preference_type,value)

            if not self.is_value_in_list(data, preference_type):
                raise Exception(f"{value} is not in favourite list")

            self.modify_preferences([data], preference_type, 'remove')
            return 'Ok'
        except SQLAlchemyError:
            raise 'Something went wrong'

    def _find_value(self, preference_type, value):

        if preference_type == 'books':
            book = self.book_service.find_one_by_title(value)
            if not book:
                raise Exception(f"Book '{value}' not found")
            return book.id
        elif preference_type == 'authors':
            author = self.book_service.find_author(value)
            if not author:
                raise Exception(f"Author '{value}' not found")
            return author.author_id
        elif preference_type == 'categories':
            if not value:
                raise Exception(f"Invalid category '{value}'")
            return value  # Categories are directly added/removed
        else:
            raise Exception(f"Unknown preference type '{preference_type}'")

    def _validate_id(self, preference_type, value):

        if preference_type == 'books':
            book = self.book_service.find_by_id(value)
            if not book:
                return False
            return True
        elif preference_type == 'authors':
            author = self.book_service.find_author_by_id(value)
            if not author:
                return False
            return True
        elif preference_type == 'categories':
            if not value:
                return False
            return value  # Categories are directly added/removed
        else:
            raise Exception(f"Unknown preference type '{preference_type}'")

    def add_to_favourite_by_id(self, value, preference_type):
        try:
            print(f"v:{value},pref:{preference_type}")
            if not self._validate_id(preference_type, value):
                raise Exception(f"{value} is not in Database")

            if self.is_value_in_list(value, preference_type):
                raise Exception(f"{value} already in favourite list")

            self.modify_preferences([value], preference_type, 'add')
            return 'Ok'
        except SQLAlchemyError:
            raise 'Something went wrong'

    def remove_from_favourite_by_id(self, value, preference_type):
        try:
            if not self.is_value_in_list(value, preference_type):
                raise Exception(f"{value} is not in favourite list")

            self.modify_preferences([value], preference_type, 'remove')
            return 'Ok'
        except SQLAlchemyError:
            raise 'Something went wrong'

    """
        Operates with single book, author, category
    """
    def add_book_to_favourite(self,title):
        return self.add_to_favourite(title,'books')

    def add_author_to_favourite(self,name):
        return self.add_to_favourite(name,'authors')

    def add_category_to_favourite(self,categories):
        return self.add_to_favourite(categories,"categories")

    def remove_book_from_favourite(self,title):
        return self.remove_from_favourite(title,'books')

    def remove_author_from_favourite(self,name):
        return self.remove_from_favourite(name,'authors')

    def remove_category_from_favourite(self,categories):
        return self.remove_from_favourite(categories,"categories")

    """
        Operates with collection of books, authors, categories
    """
    def add_books_to_favourite(self,titles):
        for title in titles: self.add_book_to_favourite(title)
        return "Ok"

    def remove_books_from_favourite(self,titles):
        for title in titles: self.remove_book_from_favourite(title)
        return "Ok"

    def add_authors_to_favourite(self, authors):
        for name in authors: self.add_author_to_favourite(name)
        return "Ok"

    def remove_authors_from_favourite(self, authors):
        for name in authors: self.remove_author_from_favourite(name)
        return "Ok"

    def add_categories_to_favourite(self, categories):
        for category in categories: self.add_category_to_favourite(category)
        return "Ok"

    def remove_categories_from_favourite(self, categories):
        for category in categories: self.remove_category_from_favourite(category)
        return "Ok"

    """
        Operates with id of single : book, author, category 
    """
    def add_book_id_to_favourite(self,title):
        return self.add_to_favourite_by_id(title,'books')

    def add_author_id_to_favourite(self,name):
        return self.add_to_favourite_by_id(name,'authors')

    def remove_book_id_from_favourite(self,title):
        return self.remove_from_favourite_by_id(title,'books')

    def remove_author_id_from_favourite(self,name):
        return self.remove_from_favourite_by_id(name,'authors')
