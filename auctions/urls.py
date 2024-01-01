from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<int:listing_id>", views.listings, name="listings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_watchlist/<int:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist/<int:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path("create", views.create_listing, name="create_listing"),
    path("add_comment/<int:listing_id>", views.comment, name="comment"),
    path("add_bid/<int:listing_id>", views.bid, name="bid"),
    path("wining_bid", views.wining_bid, name="wining_bid"),
    path("my_listings", views.my_listings, name="my_listings"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)