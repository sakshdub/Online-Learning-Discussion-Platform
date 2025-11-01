from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms

# Define the Tailwind classes from your HTML
INPUT_CLASSES = 'w-full px-4 py-2 rounded bg-gray-700 border border-gray-600 text-white focus:outline-none focus:ring-2 focus:ring-red-500'

class CustomUserCreationForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add the CSS classes to our fields
        self.fields['username'].widget.attrs.update({
            'class': INPUT_CLASSES, 
            'placeholder': 'Enter username'
        })
        self.fields['email'].widget.attrs.update({
            'class': INPUT_CLASSES, 
            'placeholder': 'Enter email address'
        })
        self.fields['role'].widget.attrs.update({
            'class': INPUT_CLASSES
        })
        #
        # --- PASSWORD LINES REMOVED ---
        # The default password fields will work fine.
        #
        
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'role') # This is correct

class CustomUserChangeForm(UserChangeForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': INPUT_CLASSES, 'placeholder': 'Enter username'})
        self.fields['email'].widget.attrs.update({'class': INPUT_CLASSES, 'placeholder': 'Enter email address'})
        self.fields['role'].widget.attrs.update({'class': INPUT_CLASSES})

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')