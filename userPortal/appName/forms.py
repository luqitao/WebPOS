from django import forms
 
class Login(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'autofocus': 'autofocus'}))
    password = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'password'}))