from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from .serializers import PizzaSerializer
from .models import Pizza
from rest_framework import status


class PizzaDetails(generics.RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'details.html'
    serializer_class = PizzaSerializer
    queryset = Pizza.objects.all()

    def get(self, request, queryset=queryset, *args, **kwargs):
        pk = self.kwargs['pk']
        if(queryset.filter(pk=pk).count()):
            pizza = queryset.get(pk=pk)
            serializer = PizzaSerializer(pizza)
            return Response({'pizza': serializer.data},
                            status=status.HTTP_200_OK)
        text = "We couldn't find the Pizza you requested."
        return Response({'text': text}, template_name='error.html',
                        status=status.HTTP_404_NOT_FOUND)
