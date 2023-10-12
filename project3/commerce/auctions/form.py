from django import forms
from django.forms import ModelForm

from .models import Listing, Comment, Bid

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "image", "categorie", "description"]

    starting_bid = forms.DecimalField(max_digits=6, decimal_places=2)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["ammount"]
        