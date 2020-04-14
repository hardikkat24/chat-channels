
from django.urls import path, re_path


from .views import  thread_view


urlpatterns = [

    re_path(r"^(?P<username>[\w.@+-]+)", thread_view),
]