from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Categories, Watchlist, Comment
from .form import ListingForm, CommentForm, BidForm


def index(request):
    listings = Listing.objects.filter(sold_to=None)
    return render(request, "auctions/index.html", {
        "listings" : listings
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
            watchlist = Watchlist(owner=user)
            watchlist.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            starting_bid = Bid(owner = request.user, ammount=form.cleaned_data["starting_bid"])
            starting_bid.save()

            new_listing = Listing(
                owner = request.user,
                title = form.cleaned_data["title"],
                description = form.cleaned_data["description"],
                image = form.cleaned_data["image"],
                bid = starting_bid
            )
            
            new_listing.save()

            new_listing.categorie.add(form.cleaned_data["categorie"].first().id)

            return HttpResponseRedirect(reverse("view_listing", args=(new_listing.id, )))
 
    listing_form = ListingForm()
    return render(request, "auctions/create_listing.html", {
        "listing_form" : listing_form
    })


def view_listing(request, id):
    if request.method == "POST":
        if "comment_form" in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                try:
                    listing = Listing.objects.get(id=id)
                except ObjectDoesNotExist:
                    return HttpResponse("The listing you are trying to comment on dose not exist")
                
                comment = Comment(owner=request.user, listing=listing, comment=form.cleaned_data["comment"])
                comment.save()

                return HttpResponseRedirect(reverse("view_listing", args=(id, )))
            
        elif "bid_form" in request.POST:
            form = BidForm(request.POST)
            if form.is_valid():
                try:
                    listing = Listing.objects.get(pk=id)
                except ObjectDoesNotExist:
                    HttpResponse("The listing you are trying to bid on dose not exist")

                current_bid = float(listing.bid.ammount)
                new_bid = float(form.cleaned_data["ammount"])

                if new_bid > current_bid:
                    new_bid_obj = Bid(ammount=new_bid, owner=request.user)
                    new_bid_obj.save()

                    listing.bid = new_bid_obj

                    listing.save()

                else:
                    return HttpResponse("Your bid must be higher then the current bid")                

                return HttpResponseRedirect(reverse("view_listing", args=(id, )))
    
    try:
        listing = Listing.objects.get(pk=id)
    except ObjectDoesNotExist:
        HttpResponse("The listing you requested dose not exist")
    try:
        categorie = list(listing.categorie.all())
    except ObjectDoesNotExist:
        categorie = None

    comment_form = CommentForm()
    bid_form = BidForm()
    
    try:
        comments = listing.comments.all()
    except ObjectDoesNotExist:
        comments = None
    
    return render(request, "auctions/view.html", {
        "listing" : listing,
        "categorie" : categorie,
        "comment_form" : comment_form,
        "comments" : comments,
        "bid_form" : bid_form,
    })


def categories(request):
    if request.method == "POST":
        pass

    categories = Categories.objects.all()
    return render(request, "auctions/categories.html", {
        "categories" : categories
    })


def category(request, id):
    listings = Categories.objects.get(pk=id).listings.all()
    category_title = Categories.objects.get(pk=id)

    return render(request, "auctions/categorie.html", {
        "listings" : listings,
        "category" : category_title
    })


@login_required
def watchlist(request):
    if request.method == "POST":
        pass

    watchlist = Watchlist.objects.get(owner=request.user).listings.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist" : watchlist
    })


@login_required
def add_to_watchlist(request, id):
    try:
        check = Watchlist.objects.get(owner=request.user).listings.get(id=id)
    except ObjectDoesNotExist:
        try:
            watchlist = Watchlist.objects.get(owner=request.user)
            listing = Listing.objects.get(id=id)

            watchlist.listings.add(listing)

        except ObjectDoesNotExist:
            return HttpResponse("The listing you are trying to add dose not exist")
    
    return HttpResponseRedirect(reverse("view_listing", args=(id, )))


@login_required
def close_listing(request, id):
    listing = Listing.objects.get(id=id)

    listing.sold_to = listing.bid.owner

    listing.save()

    return HttpResponseRedirect(reverse("view_listing", args=(id, )))


@login_required
def my_listings(request):
    listings = Listing.objects.filter(owner=request.user)
    return render(request, "auctions/my_listing.html", {
        "listings" : listings
    })
