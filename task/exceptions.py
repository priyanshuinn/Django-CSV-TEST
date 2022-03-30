from rest_framework.exceptions import APIException


class NoPermission(APIException):
    status_code = 400
    default_detail = "You don't have access to view all users details."
    default_code = "no_permission"

class WrongAuthorization(APIException):
    status_code = 401
    default_detail = "Wrong Authorization Token Provided !!!"
    default_code = "w_auth_token"