from django import forms
from .models import Profile


class SignupForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone')

    def signup(self, request, user):
        # Save your user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        # Save your profile
        profile = Profile()
        profile.user = user
        profile.phone = self.cleaned_data['phone']
        profile.save()


class EmailForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    subject = forms.CharField(max_length=30, required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 5}),
                              required=True)
