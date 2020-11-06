from .models import Applicants
from django import forms


class ApplicationForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Full-Name'}), required=True)
    contact_no = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Contact-Number'}), required=True)
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}), required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder' : 'Message'}), required=False)
    position = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Position'}), required=True)
    cv = forms.FileField(widget=forms.FileInput(attrs={'Single': True, 'type' : 'file'}), required=True)
    class Meta:
        model = Applicants
        fields = ('full_name', 'contact_no', 'email', 'message', 'position', 'cv')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Applicants.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists!")
        return email