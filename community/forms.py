from django import forms
from PIL import Image
class DiscussionForm(forms.Form):
    pass    

class CreateUserForm(forms.Form):
    pass

class EditProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(max_length=256,widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(max_length=256, required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    profile_image = forms.ImageField(required=False,widget=forms.FileInput(attrs={'class':'form-control'}))
