from django.core import mail
from django.contrib.auth.models import User
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import generics
from rest_framework.response import Response
from .forms import EmailForm
from .models import Account
from pizza.models import Pizza
from allauth.account.views import PasswordChangeView


class HomeView(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "home.html"
    pizza_list = Pizza.objects.all()

    def get(self, request):
        form = EmailForm()
        return Response({'form': form, 'pizza_list': self.pizza_list})

    def post(self, request):
        form = EmailForm(request.data)
        if form.is_valid():
            message = form.cleaned_data["first_name"] + " " +\
                form.cleaned_data["last_name"]\
                + ":" + form.cleaned_data["message"]
            mail.send_mail(request.data["subject"], message,
                           request.data["email"], ['teo.budeanu@gmail.com'])
            text = "Your email has been sent."
            return Response({'text': text})
        return Response({'form_with_errors': form,
                        'pizza_list': self.pizza_list})


class AccountView(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "account.html"
    queryset = Account.objects.all()

    def get(self, request, *args, **kwargs):
        return Response()

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        user = User.objects.get(pk=request.user.id)
        for key in data.keys():
            if hasattr(user, key):
                setattr(user, key, data.__getitem__(key))
                user.save()
        return Response()


class CustomPasswordChangeView(PasswordChangeView):
    success_url = 'account'
