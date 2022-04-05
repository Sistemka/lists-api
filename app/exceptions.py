from fastapi import HTTPException, status


class UserNotFound(HTTPException):
    def __init__(self) -> None:
        super(HTTPException, self).__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


class ListNotFound(HTTPException):
    def __init__(self) -> None:
        super(HTTPException, self).__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail="List not found"
        )


class ActionAlreadyDone(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail="Action already done"
        )


class ActionCantBeDone(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail="Action can't be done"
        )


class PermissionDenied(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail="User can't change list"
        )


class TagAlreadyExists(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail="Same tag already exists"
        )


class TagNotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="Tag not found")


class UpdateError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_304_NOT_MODIFIED, detail="Update error"
        )
