from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Works
from .serializers import WorkSerializer


class WorkViewSet(viewsets.ModelViewSet):
    queryset = Works.objects.all()
    serializer_class = WorkSerializer


# Получаем список всех произведений.
@api_view(['GET'])
def works_list(request):
    works = Works.objects.all()
    serializer = WorkSerializer(works, many=True)
    return Response(serializer.data)

