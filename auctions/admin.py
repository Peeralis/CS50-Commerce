from django.contrib import admin

# Register your models here.
from .models import Listing, User, Bid, Comment, Watchlist

# Register your models here.


    
admin.site.register(User)
admin.site.register(Listing)