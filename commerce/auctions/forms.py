from django import forms

class ListingForm(forms.Form):
    title = forms.CharField(max_length=64, widget=forms.TextInput)
    description = forms.CharField(widget=forms.Textarea)
    img = forms.ImageField()
    start_bid = forms.DecimalField(max_digits=10, decimal_places=2)

class BidForm(forms.Form):
    bid = forms.DecimalField(max_digits=10, decimal_places=2)
    