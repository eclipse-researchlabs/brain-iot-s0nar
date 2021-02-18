from functools import wraps

from flask import request

from src import app

API_KEY = app.config.get('API_KEY')


def require_api_key(view_funcion):
    """
    Checks if the incoming request has correct "x-api-key" param in its header
    """
    @wraps(view_funcion)
    def decorated_function(*args, **kwargs):
        if request.headers.get("x-api-key") and request.headers.get("x-api-key") == API_KEY:
            return view_funcion(*args, **kwargs)
        else:
            return 'forbidden', 401
    return decorated_function
