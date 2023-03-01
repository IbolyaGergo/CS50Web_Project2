from django import forms

class ListingForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput)
    description = forms.CharField(widget=forms.Textarea)
    img = forms.ImageField(required=False)
    start_bid = forms.DecimalField(decimal_places=2)