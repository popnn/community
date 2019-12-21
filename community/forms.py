from django import forms
from PIL import Image

class DiscussionForm(forms.Form):
    title = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'form-control'}))
    max_comments = forms.IntegerField(initial=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(max_length=256, required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'form-control'}))

class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
    password_verify = forms.CharField(max_length=30, widget=forms.PasswordInput) 

class EditProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(max_length=256, required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    profile_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
