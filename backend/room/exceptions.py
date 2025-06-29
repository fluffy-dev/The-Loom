from backend.libs.exceptions import NotFound, AlreadyExists

class RoomNotFound(NotFound):
    pass

class RoomLimitExceeded(AlreadyExists):
    """Raised when a user tries to create more rooms than allowed."""
    pass

class FileLimitExceeded(Exception):
    """Raised when trying to add too many files to a room."""
    pass

class FileSizeExceeded(Exception):
    """Raised when an uploaded file is too large."""
    pass