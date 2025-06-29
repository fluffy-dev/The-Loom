
class AlreadyExists(Exception):
    """
    Raised when an entity already exists or violates uniqueness rules.
    """
    pass


class NotFound(Exception):
    """
    Raised when a requested entity is not found.
    """
    pass


class PaginationError(Exception):
    """
    Raised for invalid pagination parameters (e.g., negative limit).
    """
    pass