from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserAccount, UserAddress
from .constants import GENDER_TYPE


class UserRegistrationForm(UserCreationForm):
    phone_number1 = forms.CharField(max_length=15, required=True, help_text="Primary phone number (unique).")
    phone_number2 = forms.CharField(max_length=15, required=True, help_text="Secondary phone number (unique).")
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=20)  # Updated for consistency with models.py
    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = [
            'username', 'password1', 'password2', 'first_name', 'last_name', 'email', 
            'phone_number1', 'phone_number2', 'birth_date', 'gender', 
            'street_address', 'city', 'postal_code', 'country',
        ]
        
    def save(self, commit=True):
        our_user = super().save(commit=False)
        if commit:
            our_user.save()
            phone_number1 = self.cleaned_data.get('phone_number1')
            phone_number2 = self.cleaned_data.get('phone_number2')
            gender = self.cleaned_data.get('gender')
            birth_date = self.cleaned_data.get('birth_date')
            street_address = self.cleaned_data.get('street_address')
            city = self.cleaned_data.get('city')
            postal_code = self.cleaned_data.get('postal_code')
            country = self.cleaned_data.get('country')

            UserAddress.objects.create(
                user=our_user,
                street_address=street_address,
                city=city,
                postal_code=postal_code,
                country=country,
            )

            UserAccount.objects.create(
                user=our_user,
                account_no=100000 + our_user.id,  # Generate account number
                phone_number1=phone_number1,
                phone_number2=phone_number2,
                birth_date=birth_date,
                gender=gender,
                email=our_user.email,
            )
        return our_user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500 '
                )
            })


class UserUpdateForm(forms.ModelForm):
    phone_number1 = forms.CharField(max_length=15, required=True)
    phone_number2 = forms.CharField(max_length=15, required=True)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=20)  # Updated for consistency with models.py
    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply consistent styling to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })

        if self.instance:
            try:
                user_account = self.instance.account
                user_address = self.instance.address
            except (UserAccount.DoesNotExist, UserAddress.DoesNotExist):
                user_account = None
                user_address = None

            if user_account:
                self.fields['phone_number1'].initial = user_account.phone_number1
                self.fields['phone_number2'].initial = user_account.phone_number2
                self.fields['birth_date'].initial = user_account.birth_date
                self.fields['gender'].initial = user_account.gender

            if user_address:
                self.fields['street_address'].initial = user_address.street_address
                self.fields['city'].initial = user_address.city
                self.fields['postal_code'].initial = user_address.postal_code
                self.fields['country'].initial = user_address.country

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            user_account, _ = UserAccount.objects.get_or_create(user=user)
            user_address, _ = UserAddress.objects.get_or_create(user=user)

            user_account.phone_number1 = self.cleaned_data['phone_number1']
            user_account.phone_number2 = self.cleaned_data['phone_number2']
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.gender = self.cleaned_data['gender']
            user_account.save()

            user_address.street_address = self.cleaned_data['street_address']
            user_address.city = self.cleaned_data['city']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.country = self.cleaned_data['country']
            user_address.save()

        return user

