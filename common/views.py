from http import HTTPStatus

from django.shortcuts import render
from django.views import View


class BaseView(View):
    def dispatch(self, request, *args, **kwargs):
        request.method = request.POST.get("_method", request.method).upper()
        return super().dispatch(request, *args, **kwargs)


def bad_request(request, exception):
    return render(
        request, template_name="errors/400.html", status=HTTPStatus.BAD_REQUEST
    )


def permission_denied(request, exception):
    return render(request, template_name="errors/403.html", status=HTTPStatus.FORBIDDEN)


def page_not_found(request, exception):
    return render(request, template_name="errors/404.html", status=HTTPStatus.NOT_FOUND)


def server_error(request):
    return render(
        request,
        template_name="errors/500.html",
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )
