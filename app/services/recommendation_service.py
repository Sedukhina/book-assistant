import json

from openai import OpenAI

from db.db import get_session

from services.book_service import BookService

from services.preferences_service import PreferencesService

book_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Book",
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique identifier for the book."
    },
    "title": {
      "type": "string",
      "description": "The title of the book."
    },
    "categories": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "default": [],
      "description": "List of categories associated with the book."
    },
    "author": {
      "type": "string",
      "description": "The author of the book."
    },
    "isbn": {
      "type": "string",
      "description": "The ISBN of the book."
    },
    "cover_link": {
      "type": "string",
      "description": "A link to the book's cover image."
    },
    "description": {
      "type": "string",
      "description": "A brief description of the book."
    },
    "publish_year": {
      "type": "integer",
      "description": "The year the book was published."
    }
  },
  "required": ["id", "title", "author", "isbn", "publish_year"]
}


class RecommendationService:
    def __init__(self,api_key,username):
        self.book_service = BookService(get_session())
        self.preference_service = PreferencesService(username)
        self.client = OpenAI(api_key=api_key)


        self.functions = self.create_book_service_functions()
        self.functions_map = dict()
        self.functions_map.update(self.create_book_service_map())
        # self.functions_map.update(self.create_preferences_service_map())


    def create_book_service_functions(self):
        return  [
            {
                "name": "get_books_data",
                "description": "Повертає усі книги з списку користувача",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_categories_data",
                "description": "Повертає усі категорії з списку користувача",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_authors_data",
                "description": "Повертає усіх авторів з списку користувача",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_all_data",
                "description": "Повертає спискок користувача",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "find_by_id",
                "description": "Знаходить книгу за її ідентифікатором.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "book_id": {"type": "integer", "description": "Ідентифікатор книги"}
                    },
                    "required": ["book_id"]
                }
            },
            {
                "name": "find_by_title",
                "description": "Знаходить книги за заголовком або його частиною.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Заголовок або частина заголовка книги"}
                    },
                    "required": ["title"]
                }
            },
            {
                "name": "find_author",
                "description": "Знаходить автора за ім'ям або його частиною.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Ім'я або частина імені автора"}
                    },
                    "required": ["name"]
                }
            },
            {
                "name": "find_books_by_author_name",
                "description": "Знаходить книги за іменем автора.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "author_name": {"type": "string", "description": "Ім'я автора"}
                    },
                    "required": ["author_name"]
                }
            },
            {
                "name":"recommend_books_by_title",
                "description":"Recommends similar books by provided title",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Заголовок або частина заголовка книги"}
                    },
                    "required": ["title"]
                }
            },{
                "name":"recommend_books_based_my_list",
                "description":"Recommends books based on provided preference list",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_filtered_books",
                "description": "Фільтрує книги за різними параметрами.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Заголовок книги"},
                        "categories": {"type": "array", "items": {"type": "string"}, "description": "Категорії книг"},
                        "author": {"type": "string", "description": "Ім'я автора"},
                        "published_year_from": {"type": "integer", "description": "Рік публікації від"},
                        "published_year_to": {"type": "integer", "description": "Рік публікації до"}
                    }
                }
            },
        ]

    def create_book_service_map(self):
        return {
            "find_by_title": self.book_service.find_by_title,
            "find_author": self.book_service.find_author,
            "find_books_by_author_name": self.book_service.find_books_by_author_name,
            "get_filtered_books": self.book_service.get_filtered_books,
            "get_books_data": self.preference_service.get_books_data,
            "get_categories_data": self.preference_service.get_categories_data,
            "get_authors_data": self.preference_service.get_authors_data,
            "get_all_data": self.preference_service.get_all_data,
            "recommend_books_by_title":self.recommend_books_by_title,
            "recommend_books_based_my_list":self.recommend_books_based_my_list
        }

#TODO fix error handling
    def recommend(self, user_query):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Ти асистент, який допомагає керувати базою даних книг і авторів, а також керуєш списком уподобань користувача. А також рекомендуєш книжки, авторів"},
                    {"role": "user", "content": user_query}
                ],
                functions=self.functions)
            print(response.choices[0].message.function_call)
            if response.choices[0].message.function_call:
                function_call = response.choices[0].message.function_call
                function_name = function_call.name
                function_ars = json.loads(function_call.arguments)

                print(f"call {function_call} | name {function_name} | args {function_ars}")
                if function_name in self.functions_map:
                    data = self.functions_map[function_name](**function_ars)
                    result = data

                else:
                    result = f"Oops {function_name} something went wrong."

                print(result)
                return result
        except Error as e:
            print(f"Error occured : {e}")

    def create_message(self, message, format):
        return [
            {"role": "system",
             "content": "You are a helpful assistant that provides books, authors and categories recommendations."},
            {"role": "user", "content": message + f"Return the data only in JSON format, {format}"}
        ]

    def request(self, message):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=message,
                response_format={"type": "json_object"}
            )
            raw = response.choices[0].message.content
            return json.loads(raw)
        except Error as e:
            print(f"Error occured : {e}")
            return None


    # todo add ukrainian translation
    def recommend_books_by_title(self, title):

        message = self.create_message(
            f"Recommend books similar to {title} and get books covers by isbn from openlibrary",
           book_schema)
        json_response = self.request(message)
        print(json_response)
        return json_response

    def recommend_books_based_my_list(self):
        my_preferences = self.preference_service.get_all_data()
        message = self.create_message(
            f"Recommend books based on my list of preferences",
            {"schema":book_schema,"preferences":my_preferences})
        json_response = self.request(message)
        print(json_response)
        return json_response