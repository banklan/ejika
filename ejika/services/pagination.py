from rest_framework.pagination import PageNumberPagination


class ServiceListPagination(PageNumberPagination):
    page_size = 12