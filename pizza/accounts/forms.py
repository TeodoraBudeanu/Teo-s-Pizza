from django import forms
from django.contrib.auth.models import User


class SignupForm(forms.ModelForm):

    phone = forms.CharField(max_length=10, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def signup(self, request, user):
        # Save your user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        user.account.phone = self.cleaned_data['phone']
        user.save()


class EmailForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    subject = forms.CharField(max_length=30, required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}),
                              required=True)
