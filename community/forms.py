from django import forms
from PIL import Image
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

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
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_verify = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'class': 'form-control'})) 
    captcha = ReCaptchaField(
        widget=ReCaptchaV3,
        public_key='6LfNLskUAAAAAJ8wFJXXblKm94vMO1cUiEoJ8Frv',
        private_key='6LfNLskUAAAAAEqM3Vi8fHMZ2w4KM4KLXeKbGiGP',
        )

class EditProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=256, widget=forms.TextInput(attrs={'class': 'form-control','readonly':''}))
    description = forms.CharField(max_length=256, required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    profile_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
