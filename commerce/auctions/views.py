from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, ListingModel, BidModel, CategoryModel
from .forms import *


def index(request):
    listings = ListingModel.objects.all()
    if request.user.is_authenticated:
        num_on_watchlist = request.user.watchlist.count()
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
    categories = CategoryModel.objects.all()
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            creator = request.user
            title = form.cleaned_data.get("title")
            description = form.cleaned_data.get("description")
            img = form.cleaned_data.get("img")
            start_bid = form.cleaned_data.get("start_bid")
            category_id = int(request.POST["category"])
            category = CategoryModel.objects.get(pk=category_id)
            if img:
                obj = ListingModel.objects.create(
                    creator=creator,
                    title=title,
                    description=description,
                    img=img,
                    start_bid=start_bid,
                    category=category
                )
            else:
                obj = ListingModel.objects.create(
                    creator=creator,
                    title=title,
                    description=description,
                    start_bid=start_bid,
                    category=category
                )
            obj.save()
            return HttpResponseRedirect(reverse("index"))
    form = ListingForm()
    return render(request, "auctions/create.html", {
        "form": form,
        "categories": categories
    })

# Listing page
def listing(request, listing_id):

    listing = ListingModel.objects.get(pk=listing_id)

    if request.method == "POST":
        form = BidForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            bid = form.cleaned_data.get("bid")
            if  bid < listing.start_bid:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "form": form,
                    "message": "Small bid."
                })
            else:
                request.user.watchlist.add(listing)
                obj = BidModel.objects.create(
                    user=user,
                    listing=listing,
                    bid=bid
                )
                obj.save()
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            creator_name = request.user.username
            body = comment_form.cleaned_data.get("body")
            new_comment = CommentModel.objects.create(
                creator_name=creator_name,
                listing=listing,
                body=body
            )
            new_comment.save()
            # # Create comment object but don't save to db yet
            # new_comment = comment_form.save(commit=False)
            # # Assign the current listing to the comment
            # new_comment.listing = listing
            # # Save the comment to the db
            # new_comment.save()

    # listing = ListingModel.objects.get(pk=listing_id)
    comments = listing.comments.filter(active=True)

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
    comment_form = CommentForm()

    if listing in request.user.watchlist.all():
        on_watchlist = True
    else:
        on_watchlist = False

    num_on_watchlist = request.user.watchlist.count()

    if num_of_bids > 0:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "form": form,
            "curr_bid": curr_bid,
            "num_of_bids": num_of_bids,
            "bidder": bidder,
            "on_watchlist": on_watchlist,
            "num_on_watchlist": num_on_watchlist,
            "comment_form": comment_form,
            "comments": comments
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "form": form,
            "curr_bid": curr_bid,
            "num_of_bids": num_of_bids,
            "on_watchlist": on_watchlist,
            "num_on_watchlist": num_on_watchlist,
            "comment_form": comment_form,
            "comments": comments
        })


def watch(request, listing_id):
    if request.method == "POST":
        listing = ListingModel.objects.get(pk=listing_id)
        user = request.user
        user.watchlist.add(listing)
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    

def unwatch(request, listing_id):
    if request.method == "POST":
        listing = ListingModel.objects.get(pk=listing_id)
        user = request.user
        user.watchlist.remove(listing)
        return HttpResponseRedirect(reverse("watchlist"))

def watchlist(request):
    if request.user.is_authenticated:
        watchlist = request.user.watchlist.all()
        num_on_watchlist = request.user.watchlist.count()
        return render(request, "auctions/watchlist.html", {
            "watchlist": watchlist,
            "num_on_watchlist": num_on_watchlist
        })
    
def close(request, listing_id):
    listing = ListingModel.objects.get(pk=listing_id)
    if request.method == "POST":
        listing.active = False
        print(listing.active)
        listing.winner = BidModel.objects.filter(listing__id=listing_id).last().user.id
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    
def categories(request):
    categories = CategoryModel.objects.all()
    if request.user.is_authenticated:
        num_on_watchlist = request.user.watchlist.count()
        return render(request, "auctions/categories.html", {
                "categories": categories,
                "num_on_watchlist": num_on_watchlist
            })
    return render(request, "auctions/categories.html", {
                "categories": categories
            })
    
def category(request, category_name):
    listings = ListingModel.objects.filter(category__name=category_name).all()
    if request.user.is_authenticated:
        num_on_watchlist = request.user.watchlist.count()
        return render(request, "auctions/index.html", {
            "listings": listings,
            "num_on_watchlist": num_on_watchlist
        })
    else:
        return render(request, "auctions/index.html", {
            "listings": listings
        })