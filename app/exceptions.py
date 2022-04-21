from fastapi import HTTPException, status

from utils.tools.convertions import camel_to_words


class HttpException(HTTPException):
    def __init__(self, status_code: status, detail=None) -> None:
        super().__init__(
            status_code=status_code,
            detail=detail or camel_to_words(self.__class__.__name__),
        )


class UserNotFound(HttpException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND)


class ListNotFound(HttpException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND)


class ActionAlreadyDone(HttpException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_409_CONFLICT)


class ActionCantBeDone(HttpException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN)


class PermissionDenied(HttpException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN)


class TagAlreadyExists(HttpException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_409_CONFLICT)


class TagNotFound(HttpException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND)


class UpdateError(HttpException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_409_CONFLICT)
