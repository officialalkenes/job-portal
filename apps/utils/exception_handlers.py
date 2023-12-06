from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    exception_class = exc.__class__.__name__
    print(exception_class)
    if exception_class == "AuthenticationFailed":
        response.data = {
            "error": "Invalid Login Credentials. Please Try again",
        }
    elif exception_class == "NotAuthenticated":
        response.data = {
            "error": "You need to login to Access this resource",
        }
    elif exception_class == "InvalidToken":
        response.data = {
            "error": "Authentication Token expired. Please Login again",
        }

    return response
