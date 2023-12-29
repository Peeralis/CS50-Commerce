from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Watchlist

# Complete the implementation of your auction site. You must fulfill the following requirements:

# Models: Your application should have at least three models in addition to the User model: one for auction listings, one for bids, and one for comments made on auction listings. It’s up to you to decide what fields each model should have, and what the types of those fields should be. You may have additional models if you would like.
# Create Listing: Users should be able to visit a page to create a new listing. They should be able to specify a title for the listing, a text-based description, and what the starting bid should be. Users should also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).
# Active Listings Page: The default route of your web application should let users view all of the currently active auction listings. For each active listing, this page should display (at minimum) the title, description, current price, and photo (if one exists for the listing).
# Listing Page: Clicking on a listing should take users to a page specific to that listing. On that page, users should be able to view all details about the listing, including the current price for the listing.
# If the user is signed in, the user should be able to add the item to their “Watchlist.” If the item is already on the watchlist, the user should be able to remove it.
# If the user is signed in, the user should be able to bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the user should be presented with an error.
# If the user is signed in and is the one who created the listing, the user should have the ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
# If a user is signed in on a closed listing page, and the user has won that auction, the page should say so.
# Users who are signed in should be able to add comments to the listing page. The listing page should display all comments that have been made on the listing.
# Watchlist: Users who are signed in should be able to visit a Watchlist page, which should display all of the listings that a user has added to their watchlist. Clicking on any of those listings should take the user to that listing’s page.
# Categories: Users should be able to visit a page that displays a list of all listing categories. Clicking on the name of any category should take the user to a page that displays all of the active listings in that category.
# Django Admin Interface: Via the Django admin interface, a site administrator should be able to view, add, edit, and delete any listings, comments, and bids made on the site.
# urlpatterns = [
#     path("", views.index, name="index"),
#     path("login", views.login_view, name="login"),
#     path("logout", views.logout_view, name="logout"),
#     path("register", views.register, name="register"),
#     path("<str:title>", views.listing, name="listing"),
#     path("create", views.create, name="create"),
#     path("watchlist", views.watchlist, name="watchlist"),
#     path("categories", views.categories, name="categories"),
#     path("category/<str:category>", views.category, name="category"),
#     path("bid/<str:title>", views.bid, name="bid"),
#     path("close/<str:title>", views.close, name="close"),
#     path("comment/<str:title>", views.comment, name="comment"),
#     path("watchlist/<str:title>", views.watchlist_add, name="watchlist_add"),
#     path("watchlist_remove/<str:title>", views.watchlist_remove, name="watchlist_remove")
# ]
def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", { "listings": listings })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listings(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    comments = Comment.objects.filter(listing=listing)
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        if listing.user == user:
            return render(request, "auctions/listings.html", {
                "listing": listing,
                "comments": comments,
                "watchlist": user.watchlist.all(),
                "user": user,
                "close": True
            })
        else:
            return render(request, "auctions/listings.html", {
                "listing": listing,
                "comments": comments,
                "watchlist": user.watchlist.all(),
                "user": user
            })
    else:
        return render(request, "auctions/listings.html", {
            "listing": listing,
            "comments": comments
        })
    
def watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    listings = []
    for item in watchlist:
        listings.append(item.listing)
    print(watchlist)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })
    
def add_watchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = User.objects.get(username=request.user)
    if Watchlist.objects.filter(user=user, listing=listing).exists():
        return HttpResponseRedirect(reverse("listings", args=(listing_id,)))
    watchlist = Watchlist(user=user, listing=listing)
    watchlist.save()
    return HttpResponseRedirect(reverse("listings", args=(listing_id,)))

def remove_watchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = User.objects.get(username=request.user)
    watchlist = Watchlist.objects.get(user=user, listing=listing)
    watchlist.delete()
    return HttpResponseRedirect(reverse("watchlist"))
