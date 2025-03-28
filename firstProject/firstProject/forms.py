from django import forms

class createForms(forms.Form):
    num1=forms.IntegerField(label="Input-1",widget=forms.TextInput(attrs={'class':"form-control"}))
    num2=forms.IntegerField(label="Input-2",widget=forms.TextInput(attrs={'class':"form-control"}))