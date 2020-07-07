from functools import wraps


def prevent_missing_id(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if kwargs.get('id') is None:
            kwargs['id'] = None
        return function(**kwargs)
    return wrapper
