from rest_framework.pagination import (
    PageNumberPagination,
    Response,
)


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        try:
            previous = self.page.previous_page_number()
        except Exception:
            previous = None
        return Response({
            'count': self.page.paginator.count,
            'per_page': self.page.paginator.per_page,
            'page': self.page.number,
            'next_link': self.get_next_link(),
            'previous_link': self.get_previous_link(),
            'next': self.page.next_page_number(),
            'previous': previous,
            'results': data,
        })