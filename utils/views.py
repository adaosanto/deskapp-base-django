from operator import attrgetter

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class LoginRequiredMixin(object):
    """
    Mixin to require login.
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class BasePaginator(TemplateView):
    def get_queryset(self, request, *args, **kwargs):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        draw = request.GET.get("draw")
        start = request.GET.get("start")
        length = request.GET.get("length")
        search_value = request.GET.get("search[value]")
        order_colum = int(request.GET.get("order[0][column]", 0))
        order_dir = request.GET.get("order[0][dir]")
        format = request.GET.get("f")

        if format == "json":
            if not start:
                start = 0
            if not length:
                length = 12

            page_id = (int(start) / int(length)) + 1

            objects = self.get_queryset(request, *args, **kwargs)
            order_field = self.fields[order_colum]
            if order_dir == "desc":
                order_field = "-" + order_field

            objects = objects.order_by(order_field.lower().replace(".", "__"))

            if search_value:
                querys = [
                    Q(**{f'{search_field.replace(".", "__")}__icontains': search_value})
                    for search_field in self.fields
                ]

                query = Q()

                for _query in querys:
                    query |= _query

                objects = objects.filter(query)

            objects_pagination = Paginator(objects, per_page=length)

            try:
                objects_page = objects_pagination.page(page_id)
                serialized_objects = {
                    "draw": draw,
                    "recordsTotal": objects_pagination.count,
                    "recordsFiltered": objects_pagination.count,
                    "data": [
                        [attrgetter(field.lower())(_object) for field in self.fields]
                        for _object in objects_page
                    ],
                }

                return JsonResponse(data=serialized_objects, safe=True)
            except (EmptyPage, PageNotAnInteger):
                return JsonResponse(data={"detalhes": "página solicitada não existe"})
        return super().get(request, *args, **kwargs)
