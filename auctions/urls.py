from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>/", views.listing_detail, name="listing_detail"),
    path("watchlist/<int:listing_id>/", views.watchlist, name="watchlist"),
    path("watchlist/", views.user_watchlist, name="user_watchlist"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
