from flask import redirect, render_template, session
from functools import wraps

# https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/

def login_required(f):                                  # takes another function f as an argument
    @wraps(f)                                           # preserves the original functions meta data
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:              # checks if "user_id" is in the session
            return redirect("/login")                   # if not redirects to log in page
        return f(*args, **kwargs)                       # if it is there, call the original function, with whatever arguments or
                                                        # keyword arguments passed into it

    return decorated_function                           # decorated_function is returned 
                                                        # (with the changes in this inner function) from the login_required decorator