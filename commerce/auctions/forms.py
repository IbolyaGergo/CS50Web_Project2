from django import forms
from .models import CommentModel

class ListingForm(forms.Form):
    title = forms.CharField(max_length=64, widget=forms.TextInput)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}))
    img = forms.ImageField()
    start_bid = forms.DecimalField(max_digits=10, decimal_places=2)

class BidForm(forms.Form):
    bid = forms.DecimalField(max_digits=10, decimal_places=2)

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ('body',)
    