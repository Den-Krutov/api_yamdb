from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from reviews.models import User
from .serializers import UserSerializer


class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        if self.queryset.filter(username=username, email=email).exists():
            return Response(data=request.data, status=status.HTTP_200_OK)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
