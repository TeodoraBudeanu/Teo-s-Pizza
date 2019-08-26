from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from order.models import Order
from order.serializers import OrderSerializer
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


@method_decorator(login_required, name='dispatch')
class OrderList(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'client/home.html'
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.orders_for_client(self.request.user).filter(confirmed=1)

    def get(self, request):
        queryset = self.get_queryset()
        return Response({'orders': queryset})


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
    template_name = 'client/create_new_user.html'

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
