from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import User, Listing, Bid, Comment, Watchlist

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
    bid = Bid.objects.filter(listing=listing_id).last()
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
                "bid": bid
            })
        else:
            return render(request, "auctions/listings.html", {
                "listing": listing,
                "comments": comments,
                "watchlist": user.watchlist.all(),
                "user": user,
                "bid": bid
            })
    else:
        return render(request, "auctions/listings.html", {
            "listing": listing,
            "comments": comments,
            "bid": bid
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

def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image = request.FILES["image"]
        user = User.objects.get(username=request.user)
        listing = Listing(title=title, description=description, starting_bid=starting_bid, image=image, user=user, active=True)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_listing.html")

def comment(request, listing_id):
    if request.method == "POST":
        comment = request.POST["comment"]
        user = User.objects.get(username=request.user)
        listing = Listing.objects.get(id=listing_id)
        comment = Comment(comment=comment, user=user, listing=listing)
        comment.save()
        return HttpResponseRedirect(reverse("listings", args=(listing_id,)))
    else:
        return HttpResponseRedirect(reverse("listings", args=(listing_id,)))
    
def bid(request, listing_id):
    if request.method == "POST":
        bid_amount = request.POST.get("bid")
        user = request.user
        listing = Listing.objects.get(id=listing_id)
        current_bid = Bid.objects.filter(listing=listing).last()
        current_bid_amount = current_bid.bid if current_bid else listing.starting_bid
        if float(bid_amount) > current_bid_amount:
            bid = Bid(bid=bid_amount, user=user, listing=listing)
            bid.save()
            messages.success(request, "Bid placed successfully!")
        else:
            messages.error(request, "Bid must be higher than the current bid.")

        return HttpResponseRedirect(reverse("listings", args=(listing_id,)))
    else:
        return HttpResponseRedirect(reverse("listings", args=(listing_id,)))
    
def winning_bid(request):
    listings = Listing.objects.filter(active=False)
    winning_bids = []
    for listing in listings:
        bid = Bid.objects.filter(listing=listing).last()
        if bid:
            winning_bids.append(bid)
        else: 
            winning_bids.append("No bids yet")
    winning_bids = zip(listings, winning_bids)
    return render(request, "auctions/winning_bid.html", {"winning_bids": winning_bids})

def my_listings(request):
    listings = Listing.objects.filter(user=request.user)
    bids = []
    for listing in listings:
        bid = Bid.objects.filter(listing=listing).last()
        if bid:
            bids.append(bid)
        else: 
            bids.append("No bids yet")
    bids = zip(listings, bids)
    return render(request, "auctions/my_listings.html", {"bids": bids})

def close_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.active = False
    listing.save()
    return HttpResponseRedirect(reverse("my_listings"))
