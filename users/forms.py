"""
Users app forms - Registration, Login, Profile.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import UserProfile


class RegisterForm(UserCreationForm):
    """User registration form with email."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
    first_name = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'First name (optional)'})
    )
    last_name = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Last name (optional)'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(Column('first_name', css_class='col-md-6'), Column('last_name', css_class='col-md-6')),
            'username', 'email', 'password1', 'password2',
            Submit('submit', 'Create Account', css_class='btn btn-primary btn-lg w-100 mt-3')
        )
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
            UserProfile.objects.create(user=user)
        return user


class LoginForm(AuthenticationForm):
    """Custom login form."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'username', 'password',
            Submit('submit', 'Sign In', css_class='btn btn-primary btn-lg w-100 mt-3')
        )
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProfileForm(forms.ModelForm):
    """User profile edit form."""
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself...'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.initial['first_name'] = user.first_name
            self.initial['last_name'] = user.last_name
            self.initial['email'] = user.email
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
