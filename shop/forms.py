from django import forms
from accounts.models import CustomUser, Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['city', 'street', 'street_number', 'house_number']


class CustomUserForm(forms.ModelForm):
    city = forms.CharField(max_length=255, required=False)
    street = forms.CharField(max_length=255, required=False)
    street_number = forms.CharField(max_length=20, required=False)
    house_number = forms.CharField(max_length=20, required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.address:
            self.fields['city'].initial = self.instance.address.city
            self.fields['street'].initial = self.instance.address.street
            self.fields['street_number'].initial = self.instance.address.street_number
            self.fields['house_number'].initial = self.instance.address.house_number

    def save(self, commit=True):
        user = super().save(commit=False)
        if not user.address:
            user.address = Address()
        user.address.city = self.cleaned_data['city']
        user.address.street = self.cleaned_data['street']
        user.address.street_number = self.cleaned_data['street_number']
        user.address.house_number = self.cleaned_data['house_number']
        if commit:
            user.address.save()
            user.save()
        return user
