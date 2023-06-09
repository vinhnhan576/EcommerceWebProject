# from django import forms
from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
class RegisterForm(UserCreationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs.update({
            'name':'username',
            'id':'username',
            'type':'text',
            'placeholder':'Username',
        })

        self.fields['first_name'].widget.attrs.update({
            'name':'first_name',
            'id':'first_name',
            'type':'text',
            'placeholder':'First Name',
        })

        self.fields['last_name'].widget.attrs.update({
            'name':'last_name',
            'id':'last_name',
            'type':'text',
            'placeholder':'Last Name',
        })
        
        self.fields['email'].widget.attrs.update({
            'name':'email',
            'id':'email',
            'type':'text',
            'placeholder':'Email',
        })

        self.fields['password1'].widget.attrs.update({
            'name':'password',
            'id':'password',
            'type':'password',
            'placeholder':'Password',
        })
        
        self.fields['password2'].widget.attrs.update({
            'name':'cpassword',
            'id':'cpassword',
            'type':'password',
            'placeholder':'Confirm password',
        })
        
        self.fields['address'].widget.attrs.update({
            'name':'address',
            'id':'address',
            'type':'text',
            'placeholder':'Address',
        })
        
        self.fields['phone'].widget.attrs.update({
            'name':'phone',
            'id':'phone',
            'type':'text',
            'placeholder':'Phone',
        })
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'address', 'phone']
        
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if commit:
            user.save()
        return user

