class AppError(Exception):
    status_code = 500
    detail = "internal server error"


class NotFoundError(AppError):
    status_code = 404
    detail = "resource not found"


class AlreadyExistsError(AppError):
    status_code = 409
    detail = "resource already exists"


class InvalidCredentialsError(AppError):
    status_code = 401
    detail = "invalid credentials"


class UnauthorizedError(AppError):
    status_code = 403
    detail = "not authenticated"


class ForbiddenError(AppError):
    status_code = 403
    detail = "forbidden"