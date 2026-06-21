# core/exceptions.py

class AppError(Exception):
    pass


class ResourceNotFoundError(AppError):
    pass


class AccessDeniedError(AppError):
    pass


class BusinessRuleViolationError(AppError):
    pass


class InfraStructureViolationError(AppError):
    pass
