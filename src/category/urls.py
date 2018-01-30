from django.conf.urls import url
from src.category import views

urlpatterns = [
    url(r'^$', views.CategoryList.as_view()),
    url(r'^(?P<id>[0-9]+)/$', views.CategoryDetail.as_view())
]