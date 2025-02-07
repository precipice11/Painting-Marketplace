from django.contrib import admin
from .models import User, Category, Auction_Listing, Bid, Comment


# Register your models here.

class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'starting_bid', 'image']

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Auction_Listing, AuctionListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
