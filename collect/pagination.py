from rest_framework.pagination import LimitOffsetPagination


class DataLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 30
    max_limit = 100


class FileUploadLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 30


class TeamFileLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 30