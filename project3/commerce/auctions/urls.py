from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"), 
    path("view/<int:id>", views.view_listing, name="view_listing"),
    path("categories", views.categories, name="categories"),
    path("category/<int:id>", views.category, name="category"),
    path("add_to_watchlist/<int:id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("close_listing/<int:id>", views.close_listing, name="close_listing"),
    path("my_listings", views.my_listings, name="my_listings"),
]
