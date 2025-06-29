from backend.libs.exceptions import AlreadyExists, NotFound

class UserAlreadyExist(AlreadyExists):
    pass

class UserNotFound(NotFound):
    pass