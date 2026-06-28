from celery import shared_task
from django.utils import timezone
from .models import Auction

@shared_task
def close_expired_auctions():
    """
    This task runs every minute.
    It finds all timed auctions that have passed their end_time
    and closes them, declaring the highest bidder as winner.
    """
    # Find all active timed auctions that have expired
    expired_auctions = Auction.objects.filter(
        auction_type='timed',
        status='active',
        end_time__lte=timezone.now()   # end_time is less than or equal to now
    )

    closed_count = 0
    for auction in expired_auctions:
        auction.close_auction()        # declares winner, sets status to 'closed'
        closed_count += 1
        print(f'Closed auction: {auction.product.title} | Winner: {auction.winner}')

    return f'{closed_count} auctions closed.'