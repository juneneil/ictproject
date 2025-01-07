from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Custom User Creation Form with improved design, including name and email fields.
    """

    name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': 'Enter your full name',
        }),
        label="Full Name",
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control text-center',
            'placeholder': 'Enter your email address',
            'autocomplete': 'email',
        }),
        label="Email",
    )
    
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control text-center',
            'placeholder': 'Enter your password',
        }),
        label="password1",
    )
    
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control text-center',
            'placeholder': 'Confirm your password',
        }),
        label="password2",
    )
    

    class Meta:
        model = User
        fields = ('name', 'email', 'username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control text-center',
                'placeholder': 'Enter your username',
                'autocomplete': 'username',
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control text-center',
                'placeholder': 'Enter your password',
                'autocomplete': 'new-password',
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control text-center',
                'placeholder': 'Confirm your password',
                'autocomplete': 'new-password',
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Adds Bootstrap classes and dynamic error handling.
        """
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "Full Name"  # Custom label
        self.fields['email'].label = "Email Address"  # Custom label
        self.fields['username'].label = "User Name"  # Custom label
        self.fields['password1'].label = "Create Password"
        self.fields['password2'].label = "Confirm Password"

        

    def clean_password2(self):
        """
        Custom validation to ensure password1 and password2 match.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def clean_email(self):
        """
        Custom validation to ensure email is unique.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        """
        Override save method to handle custom fields.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('name').split(' ')[0]
        user.last_name = ' '.join(self.cleaned_data.get('name').split(' ')[1:])
        if commit:
            user.save()
        return user
