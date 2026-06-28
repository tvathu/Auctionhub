from django.db import models
from django.utils import timezone
from accounts.models import User
from products.models import Product

class Auction(models.Model):
    TYPE_CHOICES = (
        ('timed', 'Timed Auction'),
        ('open', 'Open Auction'),
    )
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('active', 'Active'),
        ('closed', 'Closed'),
    )

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='auction')
    auction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)  # Only for timed auctions
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_auctions')

    def __str__(self):
        return f"Auction for {self.product.title}"

    def get_highest_bid(self):
        return self.bids.order_by('-amount').first()

    def get_current_price(self):
        highest = self.get_highest_bid()
        return highest.amount if highest else self.product.starting_price

    def is_expired(self):
        if self.auction_type == 'timed' and self.end_time:
            return timezone.now() > self.end_time
        return False

    def close_auction(self):
        self.status = 'closed'
        highest_bid = self.get_highest_bid()
        if highest_bid:
            self.winner = highest_bid.bidder
        self.save()


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    placed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-amount']

    def __str__(self):
        return f"{self.bidder.username} bid ₹{self.amount} on {self.auction.product.title}"