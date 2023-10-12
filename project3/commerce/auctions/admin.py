from django.contrib import admin

from .models import User, Categories, Bid, Listing, Watchlist, Comment

admin.site.register(User)
admin.site.register(Watchlist)
admin.site.register(Categories)
admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(Comment)
