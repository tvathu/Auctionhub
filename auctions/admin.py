from django.contrib import admin
from .models import Auction, Bid

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ['product', 'auction_type', 'status', 'get_current_price', 'winner', 'end_time']
    list_filter = ['auction_type', 'status']
    actions = ['close_selected_auctions']

    def get_current_price(self, obj):
        return f'₹{obj.get_current_price()}'
    get_current_price.short_description = 'Current Price'

    def close_selected_auctions(self, request, queryset):
        for auction in queryset:
            auction.close_auction()
        self.message_user(request, 'Selected auctions have been closed.')
    close_selected_auctions.short_description = 'Close selected auctions'

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['bidder', 'auction', 'amount', 'placed_at']
    list_filter = ['placed_at']