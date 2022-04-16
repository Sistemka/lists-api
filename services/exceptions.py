class UserNotFoundError(Exception):
    pass


class ListNotFoundError(Exception):
    pass


class ListItemNotFoundError(Exception):
    pass


class TagNotFoundError(Exception):
    pass


class ActionAlreadyDoneError(Exception):
    pass


class ActionCantBeDoneError(Exception):
    pass


class InvalidDataError(Exception):
    pass


class PermissionDeniedError(Exception):
    pass


class TagAlreadyExistsError(Exception):
    pass


class DeleteError(Exception):
    pass


class UpdateError(Exception):
    pass
