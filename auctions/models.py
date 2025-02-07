from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Auction_Listing', blank=True, related_name='watched_by')

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

class Auction_Listing(models.Model):
    title = models.CharField(max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    is_active = models.BooleanField(default=True)
    description = models.TextField()
    starting_bid = models.IntegerField()
    current_price = models.IntegerField(null=True, blank=True)  # Track the current bid
    image = models.ImageField(upload_to='listing_images/', blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="listings")

    def __str__(self):
        return self.title
    

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, related_name="bids")
    bid_amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid by {self.user.username} for {self.listing.title}"
    


class Comment(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, related_name="comments")
    text=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.listing.title}"


