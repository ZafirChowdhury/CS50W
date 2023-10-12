from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    
    def __str__(self):
        return f"{self.username}"


class Categories(models.Model):
    title  = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    ammount = models.DecimalField(max_digits=12, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"${self.ammount}"
    

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    categorie = models.ManyToManyField(Categories, related_name="listings")
    

    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.URLField(null=True, blank=True)

    bid = models.OneToOneField(Bid, on_delete=models.PROTECT, related_name="listing")
    post_time = models.DateTimeField(auto_now_add=True)

    sold_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="p", default=None, null=True, blank=True)
    
    def __str__(self):
        return f"{self.title}"


class Watchlist(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="watchlist")
    listings = models.ManyToManyField(Listing, related_name="listings", null=True, blank=True)

    def __str__(self):
        return f"{self.owner}"


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE ,related_name="comments")

    comment = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.owner} : {self.comment}"
