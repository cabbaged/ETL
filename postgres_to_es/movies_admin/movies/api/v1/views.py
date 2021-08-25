from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        return Filmwork.objects.all()

    @staticmethod
    def render_to_response(context, **__):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        return {'count': paginator.count,
                'total_pages': paginator.num_pages,
                'prev': page.previous_page_number() if page.has_previous() else 0,
                'next': page.next_page_number() if page.has_next() else 0,
                'object_list': list(queryset.values())}


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs):
        f = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        fields = ('id', 'title', 'description', 'certificate', 'rating', 'type')
        return model_to_dict(f, fields=fields)
