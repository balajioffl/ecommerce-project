from rest_framework.pagination import PageNumberPagination
from .constants import MAX_PAGE_SIZE, DEFAULT_PAGE_SIZE


class DefaultPagination(PageNumberPagination):
    """
    Default pagination used across the project.
    """

    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = "page_size"
    max_page_size = MAX_PAGE_SIZE