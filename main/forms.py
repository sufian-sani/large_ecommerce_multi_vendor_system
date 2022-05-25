from django.forms import ModelForm
from django import forms
from checkout.models import Order_Table


class Upload_Deposit_slip(ModelForm):
    class Meta:
        model = Order_Table
        fields = ['Deposit_slip']
        
    Deposit_slip = forms.FileField(required=True)