from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from imei.serializers import TokenTGSerializer


class TokenTGPostView(APIView):
    """Вьюшка для передачи токена пользователем"""
    def post(self, request):
        serializer = TokenTGSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            return Response({'name': name}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
