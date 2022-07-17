from cProfile import label
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile
from movies.models import Review

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    about = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Describe yourself to the world', 'rows': '3'}))
    class Meta:
        model = Profile
        fields = ['image', 'about']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['about'].required = False


class ShareYourThoughts(forms.ModelForm):
    RATINGS = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    ]
    body = forms.CharField(
        label='Write your review: ',
        widget=forms.Textarea(attrs={'rows': '10', 'class': 'txt-format'}) 
    )
    tldr = forms.CharField(
        label='TLDR: ',
        widget=forms.Textarea(attrs={'rows': '2', 'class': 'txt-format'}),
        help_text='Please, write a summary of your review in 120 characters.' 
    )
    title = forms.CharField(
        label='Title: '
    )
    rating = forms.CharField(
        label='Rate the movie: ',
        widget=forms.Select(
            choices=RATINGS,
            attrs={'class': 'form-select'}
        )
    )
    class Meta:
        model = Review
        fields = ['title','body', 'tldr', 'rating']