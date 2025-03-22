from django import forms

class PaymentForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    card_number = forms.CharField(max_length=16, min_length=16)
    expiry_date = forms.CharField(max_length=5)  # MM/YY format
    cvv = forms.CharField(max_length=3, min_length=3)