from django import forms
from .models import Auction, Bid

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['auction_type', 'end_time']
        widgets = {
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']

    def __init__(self, *args, auction=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.auction = auction
        if auction:
            min_bid = auction.get_current_price() + 500
            self.fields['amount'].widget.attrs.update({
                'min': str(min_bid),
                'step': '100',
                'placeholder': f'Minimum bid: ₹{min_bid}'
            })

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if self.auction and amount <= self.auction.get_current_price():
            raise forms.ValidationError(
                f'Your bid must be greater than ₹{self.auction.get_current_price()}'
            )
        return amount