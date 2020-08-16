from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>/", views.entryPage, name="entry"),
    path("search/", views.searchEntry, name="search"),
    path("create/", views.create, name="create"),
    path("edit/<str:title>/", views.edit, name="edit"),
]
