from django.core.mail import send_mail
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .forms import EmailForm


class Home(GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "home.html"

    def get(self, request):
        form = EmailForm()
        return Response({'form': form})

    def post(self, request):
        form = EmailForm(request.data)
        if form.is_valid():
            message = form.cleaned_data["first_name"] + " " +\
                form.cleaned_data["last_name"]\
                + ":" + form.cleaned_data["message"]
            send_mail(request.data["subject"], message, request.data["email"],
                      ['teo.budeanu@gmail.com'])
            text = "Your email has been sent."
            return Response({'text': text})
        return Response({'form_with_errors': form})
