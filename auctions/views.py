from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Auction, Bid
from .forms import AuctionForm, BidForm
from products.models import Product

@login_required
def create_auction(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk, seller=request.user)
    if hasattr(product, 'auction'):
        messages.error(request, 'This product already has an auction.')
        return redirect('product_detail', pk=product_pk)
    if request.method == 'POST':
        form = AuctionForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.product = product
            auction.save()
            messages.success(request, 'Auction created!')
            return redirect('auction_detail', pk=auction.pk)
    else:
        form = AuctionForm()
    return render(request, 'auctions/auction_form.html', {'form': form, 'product': product})

def auction_detail(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    bid_form = BidForm(auction=auction)
    bids = auction.bids.select_related('bidder').order_by('-amount')[:10]
    return render(request, 'auctions/auction_detail.html', {
        'auction': auction,
        'bid_form': bid_form,
        'bids': bids,
    })

@login_required
def place_bid(request, pk):
    auction = get_object_or_404(Auction, pk=pk)

    if auction.status != 'active':
        messages.error(request, 'This auction is no longer active.')
        return redirect('auction_detail', pk=pk)

    if auction.product.seller == request.user:
        messages.error(request, 'Sellers cannot bid on their own products.')
        return redirect('auction_detail', pk=pk)

    if auction.is_expired():
        auction.close_auction()
        messages.error(request, 'This auction has ended.')
        return redirect('auction_detail', pk=pk)

    if request.method == 'POST':
        form = BidForm(request.POST, auction=auction)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.auction = auction
            bid.bidder = request.user
            bid.save()
            messages.success(request, f'Bid of ₹{bid.amount} placed successfully!')
        else:
            for error in form.errors.values():
                messages.error(request, error)

    return redirect('auction_detail', pk=pk)

@login_required
def close_auction(request, pk):
    auction = get_object_or_404(Auction, pk=pk, product__seller=request.user)
    if auction.auction_type == 'open' and auction.status == 'active':
        auction.close_auction()
        messages.success(request, f'Auction closed! Winner: {auction.winner}')
    return redirect('auction_detail', pk=pk)

def auction_list(request):
    auctions = Auction.objects.filter(status='active').select_related('product')
    return render(request, 'auctions/auction_list.html', {'auctions': auctions})

def auction_status(request, pk):
    """
    Returns current auction data as JSON.
    Called by JavaScript every 3 seconds.
    """
    auction = get_object_or_404(Auction, pk=pk)
    highest_bid = auction.get_highest_bid()

    data = {
        'current_price': str(auction.get_current_price()),
        'bid_count': auction.bids.count(),
        'status': auction.status,
        'winner': auction.winner.username if auction.winner else None,
        'latest_bidder': highest_bid.bidder.username if highest_bid else None,
        'latest_bid_time': highest_bid.placed_at.strftime('%d %b %Y, %H:%M:%S') if highest_bid else None,
    }
    return JsonResponse(data)