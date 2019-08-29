from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


def welcome(request):
    return render(request, 'welcome.html')


class CheckUsername(generics.RetrieveAPIView):

    def get(self, request):
        username = request.GET.get('username')
        if User.objects.filter(username=username).count() > 0:
            return JsonResponse("1", safe=False)
        else:
            return JsonResponse("0", safe=False)


class CheckEmail(generics.RetrieveAPIView):

    def get(self, request):
        email = request.GET.get('email')
        if User.objects.filter(email=email).count() > 0:
            return JsonResponse("1", safe=False)
        else:
            return JsonResponse("0", safe=False)


class CreateNewUser(generics.ListCreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'create_new_user.html'

    def get(self, request):
        return Response()

    def post(self, request):
        def get_queryset():
            return User.objects.all
        dict = request.data.dict()

        errors = []

        try:
            user = User.objects.create_user(dict["username"], dict["email"],
                                            dict["password"])
            user.first_name = dict["first_name"]
            user.last_name = dict["last_name"]
            user.phone = dict["phone"]
            user.save()
        except IntegrityError:
            errors.append("This username is already taken.")
        if len(errors) > 0:
            return Response({'errors': errors})
        else:
            return redirect('client_login')
