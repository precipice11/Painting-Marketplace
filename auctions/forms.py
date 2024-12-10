from django import forms
from .models import Category

class createListing(forms.Form):
    title = forms.CharField(label='Listing Title', max_length=64)
    description = forms.CharField(
        label='Description', 
        max_length=512, 
        widget=forms.Textarea
    )
    starting_bid = forms.IntegerField(label='Starting Bid')
    image = forms.ImageField(label='Upload Image', required=False)  # Change to ImageField
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Category",
        empty_label="Select a Category",
        widget=forms.Select
    )
