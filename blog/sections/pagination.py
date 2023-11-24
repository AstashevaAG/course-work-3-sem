from rest_framework import pagination

class ArticlePagination(pagination.PageNumberPagination):
    page_size = 3

class CommentPagination(pagination.PageNumberPagination):
    page_size = 10