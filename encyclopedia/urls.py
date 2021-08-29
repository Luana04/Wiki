from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add, name="add"),
    path("wiki/<title>", views.page, name="page"),
    path("random", views.random, name="random"),
    path('search/', views.search, name='search_results'),
]

