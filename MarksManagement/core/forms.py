from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from .models import Marks

class UserRegistration(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']
    

class UserLoginForm(AuthenticationForm):
    pass

class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = ['student', 'subject', 'marks_obtained', 'total_marks']