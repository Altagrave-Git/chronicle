from users.models import User
from main.settings import SENDGRID_API_KEY
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from rest_framework.decorators import authentication_classes, parser_classes, renderer_classes, throttle_classes, permission_classes, api_view
from rest_framework import permissions, parsers, renderers, throttling, authentication
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer
from rest_framework import status


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
@parser_classes([parsers.JSONParser])
def messages(request):
    if request.method == 'GET':
        message_set = Message.objects.order_by("timestamp").reverse().all()

        if message_set.exists():
            serializer = MessageSerializer(message_set, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:
            return Response({'message': 'no content'}, status=status.HTTP_200_OK)
        

@api_view(['PUT', 'DELETE'])
@permission_classes([permissions.IsAdminUser])
@parser_classes([parsers.JSONParser])
def message(request, id):
    try:
        message = Message.objects.get(id=id)
    except: return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        message.is_new = False
        message.save()
        return Response({"is_new": False}, status=status.HTTP_200_OK)
    
    if request.method == 'DELETE':
        message.delete()
        return Response(status=status.HTTP_200_OK)
        

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@throttle_classes([throttling.AnonRateThrottle, throttling.UserRateThrottle])
@parser_classes([parsers.JSONParser])
def send(request):
    sender = request.data.get('sender')
    contact = request.data.get('contact')
    content = request.data.get('content')

    if sender and contact and content:
        print(request.data)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

        message = Mail(
            from_email = 'damon.j.turcotte@gmail.com',
            to_emails = 'damon.j.turcotte@gmail.com',
            subject = sender + ' // ' + contact,
            html_content=content
        )

        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            print(response)

        except Exception as e:
            print(e.message)
            return Response({'message': 'A problem was encountered.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'success'}, status=status.HTTP_200_OK)
    
    else:
        Response({'message': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
@parser_classes([parsers.JSONParser])
def check(request):
    if request.method == 'GET':
        if Message.objects.filter(is_new=True).exists():
            return Response(True, status=status.HTTP_200_OK)
        else:
            return Response(False, status=status.HTTP_200_OK)