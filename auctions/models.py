from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    watchlist = models.ManyToManyField('Listing', blank=True, related_name='watchlist')
    def __str__(self):
        return f"{self.username}"
    
class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/', blank=True)
    category = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.title}"
    
class Bid(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bid_user')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bid_listing')
    def __str__(self):
        return f"{self.bid}"
    
class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comment_listing')
    def __str__(self):
        return f"{self.comment}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist_user')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='watchlist_listing')
    def __str__(self):
        return f"{self.user} - {self.listing}"
    
    
