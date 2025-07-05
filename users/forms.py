from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """User registration form with email as primary field"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Enter your email address'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Enter your last name'
        })
    )
    gender = forms.ChoiceField(
        choices=[('', 'Select Gender')] + User.GENDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'select select-bordered w-full'
        })
    )
    country = forms.ChoiceField(
        choices=[('', 'Select Country')] + User.COUNTRY_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'select select-bordered w-full'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'gender', 'country', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.gender = self.cleaned_data.get('gender', '')
        user.country = self.cleaned_data.get('country', '')
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile information"""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 
            'phone_number', 'date_of_birth', 'gender', 'country', 
            'learning_goals'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Enter your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Enter your last name'
            }),
            'username': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Optional username for easy login'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input input-bordered w-full',
                'readonly': True,  # Email should not be editable
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': '+233123456789'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'input input-bordered w-full',
                'type': 'date'
            }),
            'gender': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'country': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'learning_goals': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 3,
                'placeholder': 'What do you hope to achieve with your learning?'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add empty option for optional fields
        self.fields['gender'].choices = [('', 'Select Gender')] + list(User.GENDER_CHOICES)
        self.fields['country'].choices = [('', 'Select Country')] + list(User.COUNTRY_CHOICES)
        
        # Make some fields optional
        self.fields['username'].required = False
        self.fields['phone_number'].required = False
        self.fields['date_of_birth'].required = False
        self.fields['gender'].required = False
        self.fields['country'].required = False
        self.fields['learning_goals'].required = False

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Check if username is already taken by another user
            if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("This username is already taken.")
        return username


class PasswordChangeForm(forms.Form):
    """Form for changing user password"""
    
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Enter your current password'
        }),
        label='Current Password'
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Enter new password'
        }),
        label='New Password',
        min_length=8
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Confirm new password'
        }),
        label='Confirm New Password'
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError("Current password is incorrect.")
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError("New passwords don't match.")
        
        return cleaned_data

    def save(self):
        new_password = self.cleaned_data['new_password1']
        self.user.set_password(new_password)
        self.user.save()
        return self.user
