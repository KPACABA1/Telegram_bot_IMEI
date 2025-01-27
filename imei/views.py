import os
import json
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from imei.serializers import TokenTGSerializer


class TokenTGPostView(APIView):
    """Вьюшка для передачи токена пользователем"""
    def post(self, request):
        serializer = TokenTGSerializer(data=request.data)
        if serializer.is_valid():
            # подключение к сервису https://imeicheck.net/
            url = 'https://api.imeicheck.net/v1/checks'
            token_imeicheck = os.getenv('token_imeicheck')
            headers = {
                'Authorization': 'Bearer ' + token_imeicheck,
                'Content-Type': 'application/json'
            }
            body = json.dumps({
                "deviceId": serializer.validated_data['imei'],
                "serviceId": 12
            })
            response = requests.post(url, headers=headers, data=body)

            # вывод информации по IMEI
            return Response({'imei': response.json()['properties']}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
