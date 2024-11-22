from django import forms
from .models import Transaction
from accounts.models import UserAccount

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount','transaction_type']
        
    def __init__(self,*args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True #ai field disable thakbe 
        self.fields['transaction_type'].widget = forms.HiddenInput() #user the hide kora thakbe
        
    def save(self, commit = True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()
    
class DepositForm(TransactionForm):
    def clean_amount(self):
        min_deposit_amount = 20
        amount = self.cleaned_data.get('amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} Tk'
            )
            
        return amount
    
class WinthdrawForm(TransactionForm):
    
    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 500
        balance = account.balance
        amount = self.cleaned_data.get('amount')
        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at least {min_withdraw_amount} $'
            )
            
            
        if amount > balance:
            raise forms.ValidationError(
                f'You have {balance} $ in your account. '
                f'You can not withdrow more than your account balance '
            )
        return amount
    
