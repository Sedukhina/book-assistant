from flask import Blueprint

from routes.api.books_api import books_api

from routes.api.authors_api import authors_api

from routes.api.user_api import user_api

from routes.api.preferences_routes import preferences_api

api_routes = Blueprint('api',__name__,url_prefix='/api')

api_routes.register_blueprint(books_api)
api_routes.register_blueprint(authors_api)
api_routes.register_blueprint(user_api)
api_routes.register_blueprint(preferences_api)
