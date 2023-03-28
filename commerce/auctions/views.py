from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, ListingModel, BidModel
from .forms import *


def index(request):
    listings = ListingModel.objects.all()
    if request.user.is_authenticated:
        num_on_watchlist = request.user.watchlist.count()
        # print(request.user.watchlist.all())
        return render(request, "auctions/index.html", {
            "listings": listings,
            "num_on_watchlist": num_on_watchlist
        })
    else:
        return render(request, "auctions/index.html", {
            "listings": listings
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


# Create a new listing
def create(request):

    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            description = form.cleaned_data.get("description")
            img = form.cleaned_data.get("img")
            start_bid = form.cleaned_data.get("start_bid")
            if img:
                obj = ListingModel.objects.create(
                    title=title,
                    description=description,
                    img=img,
                    start_bid=start_bid
                )
            else:
                obj = ListingModel.objects.create(
                    title=title,
                    description=description,
                    start_bid=start_bid
                )
            obj.save()
            return HttpResponseRedirect(reverse("index"))
    form = ListingForm()
    return render(request, "auctions/create.html", {
        "form": form
    })


def listing(request, listing_id):

    if request.method == "POST":
        form = BidForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            listing = ListingModel.objects.get(pk=listing_id)
            bid = form.cleaned_data.get("bid")
            if  bid < listing.start_bid:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "form": form,
                    "message": "Small bid."
                })
            else:
                obj = BidModel.objects.create(
                    user=user,
                    listing=listing,
                    bid=bid
                )
                obj.save()
                form = BidForm()
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
                # return HttpResponseRedirect(reverse('create_rating', args=(video_id,)))

    listing = ListingModel.objects.get(pk=listing_id)

    if BidModel.objects.filter(listing__id=listing_id):
        num_of_bids = BidModel.objects.filter(listing__id=listing_id).count()
        bidder = BidModel.objects.filter(listing__id=listing_id).last().user
    else:
        num_of_bids = 0

    if num_of_bids > 0:
        curr_bid = BidModel.objects.filter(listing__id=listing_id).last()
    else:
        curr_bid = ListingModel.objects.get(pk=listing_id).start_bid
    form = BidForm()

    if listing in request.user.watchlist.all():
        on_watchlist = True
    else:
        on_watchlist = False

    if num_of_bids > 0:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "form": form,
            "curr_bid": curr_bid,
            "num_of_bids": num_of_bids,
            "bidder": bidder,
            "on_watchlist": on_watchlist
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "form": form,
            "curr_bid": curr_bid,
            "num_of_bids": num_of_bids,
            "on_watchlist": on_watchlist
        })


def watch(request, listing_id):
    if request.method == "POST":
        listing = ListingModel.objects.get(pk=listing_id)
        user = request.user
        user.watchlist.add(listing)
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
