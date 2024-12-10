from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages


from .models import User, Category, Auction_Listing, Bid, Comment
from .forms import createListing

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Auction_Listing.objects.all(),
        "comments": Comment.objects.all(),

    })


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

def create(request):        
    if request.method == "POST":
        form = createListing(request.POST, request.FILES)
        if form.is_valid():
            # Save the new listing
            listing = Auction_Listing(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                starting_bid=form.cleaned_data["starting_bid"],
                image=form.cleaned_data["image"],
                category=form.cleaned_data["category"]
            )
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = createListing()

    return render(request, "auctions/create.html", {
        "form": form,
    })

def listing_detail(request, listing_id):
    listing = Auction_Listing.objects.get(pk=listing_id)
    return render(request, "auctions/listing_detail.html", {
        "listing": listing,
    })


@login_required
def watchlist(request, listing_id):
    listing = get_object_or_404(Auction_Listing, pk=listing_id)
    if listing in request.user.watchlist.all():
        # Remove from watchlist if already there
        request.user.watchlist.remove(listing)
    else:
        # Add to watchlist if not already there
        request.user.watchlist.add(listing)

    return HttpResponseRedirect(reverse('listing_detail', args=[listing_id]))

@login_required
def user_watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlist.all(),
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories":Category.objects.all()
    })

def category_page(request, category):
    selected_category = get_object_or_404(Category, name=category)
    listings = Auction_Listing.objects.filter(category=selected_category)
    return render(request, "auctions/category_page.html", {
        "category": selected_category,
        "listings": listings
    })



def bidding(request, user_id):
    if request.method == "POST":
        user = User.objects.get(pk=user_id)
        listing_id = request.POST.get("listing_id")
        bid_amount = int(request.POST.get("bid", 0))

        # Fetch the listing
        listing = Auction_Listing.objects.get(pk=listing_id)

        # Validate the bid
        highest_bid = listing.bids.order_by("-bid_amount").first()
        if bid_amount < listing.starting_bid:
            messages.error(request, "Your bid must be at least as large as the starting bid.")
        elif highest_bid and bid_amount <= highest_bid.bid_amount:
            messages.error(request, "Your bid must be greater than the current highest bid.")
        else:
            # Create a new bid
            Bid.objects.create(
                user=user,
                listing=listing,
                bid_amount=bid_amount
            )
            # Update the listing's current price
            listing.current_price = bid_amount
            listing.save()

            messages.success(request, "Your bid was placed successfully!")

        return redirect("listing_detail", listing_id=listing_id)
