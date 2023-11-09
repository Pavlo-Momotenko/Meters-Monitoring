from django.conf.urls import handler400, handler403, handler404, handler500
from django.urls import path

from meters.views import MetersView

handler400 = "common.views.bad_request"
handler403 = "common.views.permission_denied"
handler404 = "common.views.page_not_found"
handler500 = "common.views.server_error"

urlpatterns = [
    path("", MetersView.as_view(), name="main"),
]
