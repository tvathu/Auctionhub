from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from auctions.models import Auction

@login_required
def payment_page(request, auction_pk):
    auction = get_object_or_404(Auction, pk=auction_pk)

    # Only the winner can access the payment page
    if request.user != auction.winner:
        messages.error(request, 'Only the auction winner can access this page.')
        return redirect('auction_detail', pk=auction_pk)

    # Only show payment page if auction is closed
    if auction.status != 'closed':
        messages.error(request, 'This auction is still active.')
        return redirect('auction_detail', pk=auction_pk)

    return render(request, 'payments/payment_page.html', {
        'auction': auction,
        'amount': auction.get_current_price(),
    })

@login_required
def payment_cancel(request, auction_pk):
    # Just redirect back to the auction page
    messages.info(request, 'Payment cancelled. You can try again anytime.')
    return redirect('auction_detail', pk=auction_pk)