from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("random/", views.random_page, name="random_page"),
    path("new/", views.new, name="new"),
    path("edit/", views.edit, name="edit"),
    path("edit_post/", views.edit_post, name="edit_post"),
    
    path("<str:wiki>/", views.entry, name="entry"),
    path("search/<str:wiki>/", views.entry, name="search"),
    path("random/<str:wiki>/", views.entry, name="search"),
    path("new/<str:wiki>", views.new, name="new"),
    path("edit/<str:wiki>/", views.edit, name="edit"),
    path("edit_post/<str:wiki>/", views.edit_post, name="edit_post"),
]
