from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


def custom_response(data=None, message="", status=200):
    return Response({"message": message, "data": data, "status": status}, status)
