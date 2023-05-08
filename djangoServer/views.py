from rest_framework.response import Response
from rest_framework import request
from rest_framework.decorators import api_view

@api_view(['GET'])
def chronicle(request):
    return Response({
        'message': 'Welcome to Chronicle API'
    })
