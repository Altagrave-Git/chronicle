from .serializers import UserSerializer
from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework import status, permissions, throttling
from users.models import User
from rest_framework.decorators import permission_classes, api_view, authentication_classes, throttle_classes
import requests
import random
import string
import base64
import hashlib
from main import settings
import requests
import jwt
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.models import AccessToken

CLIENT_ID = settings.CLIENT_ID
CLIENT_SECRET = settings.CLIENT_SECRET
REDIRECT_URI = settings.REDIRECT_URI

CODE_VERIFIER = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))
CODE_VERIFIER = base64.urlsafe_b64encode(CODE_VERIFIER.encode('utf-8'))

CODE_CHALLENGE = hashlib.sha256(CODE_VERIFIER).digest()
CODE_CHALLENGE = base64.urlsafe_b64encode(CODE_CHALLENGE).decode('utf-8').replace('=', '')

auth_url = "https://echonetwork.app/o/authorize/?response_type=code&code_challenge={}&code_challenge_method=S256&client_id={}&redirect_uri={}".format(CODE_CHALLENGE, CLIENT_ID, REDIRECT_URI)


@permission_classes([permissions.AllowAny])
@api_view(["GET", "POST"])
@authentication_classes([])
@throttle_classes([throttling.AnonRateThrottle, throttling.UserRateThrottle])
def auth_view(request):
    if request.method == "GET":
        # set the code verifier in the session for later use
        verifier = jwt.encode({"verifier": CODE_VERIFIER.decode('utf-8')}, CLIENT_SECRET, algorithm="HS256")
        request.session["code_verifier"] = verifier
        return Response({"auth_url": auth_url}, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        # retrieve the authorization code from the request and the code verifier from the session
        code = request.data.get("code")
        verifier = request.session.get("code_verifier")
        verifier = jwt.decode(verifier, CLIENT_SECRET, algorithms=["HS256"])
        verifier = verifier.get("verifier").encode('utf-8')
        request.session["code_verifier"] = None

        if code and verifier:
            # use the authorization code to retrieve an id token and access token from Echo Network
            headers = {
                "Cache-Control": "no-cache",
                "Content-Type": "application/x-www-form-urlencoded"
            }

            data = {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
                "code_verifier": verifier,
                "redirect_uri": REDIRECT_URI,
                "grant_type": "authorization_code",
            }

            auth_request = requests.post("https://echonetwork.app/o/token/", headers=headers, data=data)

            # pull tokens from the response
            access_token = auth_request.json().get("access_token")
            refresh_token = auth_request.json().get("refresh_token")
            token_type = auth_request.json().get("token_type")
            expires_in = auth_request.json().get("expires_in")
            scope = auth_request.json().get("scope")
            id_token = auth_request.json().get("id_token")

            # decode the id token
            decrypted_id_token = jwt.decode(
                id_token,
                key=CLIENT_SECRET,
                algorithms=["HS256"],
                options={"verify_signature": False}
            )

            # hash the access token (HS256)
            access_token_hash = hashlib.sha256(access_token.encode('utf-8')).digest()

            # take the first half of the hash
            access_token_hash = access_token_hash[:len(access_token_hash)//2]

            # base64 encode the access token hash
            access_token_hash = base64.urlsafe_b64encode(access_token_hash).decode('utf-8').replace('=', '')

            # verify the access token hash and audience
            if access_token_hash != decrypted_id_token.get("at_hash"):
                return Response(data="Invalid access token hash", status=status.HTTP_400_BAD_REQUEST)
            if decrypted_id_token.get("aud") != CLIENT_ID:
                return Response(data="Invalid client", status=status.HTTP_400_BAD_REQUEST)

            # retrieve user data from the id token
            username = decrypted_id_token.get("preferred_username")
            first_name = decrypted_id_token.get("given_name")
            last_name = decrypted_id_token.get("family_name")
            email = decrypted_id_token.get("email")
            avatar = decrypted_id_token.get("picture")

            # Hash the id token to generate a single-use id for the user
            active_session = hashlib.sha256(id_token.encode('utf-8')).hexdigest()

            # create or retrieve the user
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.avatar = avatar
                user.access_token = access_token
                user.refresh_token = refresh_token
                user.id_token = id_token
                user.token_type = token_type
                user.expires_in = expires_in
                user.scope = scope
                user.active_session = active_session
                user.save()

            else:
                user = User(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    avatar=avatar,
                    access_token=access_token,
                    refresh_token=refresh_token,
                    id_token=id_token,
                    token_type=token_type,
                    expires_in=expires_in,
                    scope=scope,
                    active_session=active_session
                )
                user.save()

            # login the user
            login(request, user)

            # set token hash in the session for later use
            request.session["active_session"] = active_session

            # return the user data
            serializer = UserSerializer(user)
            data = serializer.data

            return Response(data=data, status=status.HTTP_200_OK)
            
        else:
            return Response(data="No code or verifier provided", status=status.HTTP_400_BAD_REQUEST)
        
    else:
        return Response(data="Invalid request", status=status.HTTP_400_BAD_REQUEST)
    

@permission_classes([permissions.AllowAny])
@api_view(["GET"])
@authentication_classes([])
def check_session(request):
    if request.method == "GET":
        # retrieve the active session variable from the session
        active_session = request.session.get("active_session")

        if active_session:
            # retrieve the user from the active session variable
            user = User.objects.get(active_session=active_session)

            # check if the session is still valid
            if user.expires_at < timezone.now():
                del request.session["active_session"]
                return Response(data="Token expired", status=status.HTTP_200_OK)

            login(request, user)

            # return user data
            serializer = UserSerializer(user)
            data = serializer.data

            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(data="No active session", status=status.HTTP_200_OK)
    else:
        return Response(data="Invalid request", status=status.HTTP_400_BAD_REQUEST)

@permission_classes([permissions.AllowAny])
@api_view(["POST"])
def logout_view(request):
    token = request.data.get('token')

    if token:
        user = User.objects.get(access_token=token)
        refresh = user.refresh_token
        oidc = user.id_token

        headers = {
            "Cache-Control": "no-cache",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "token": token,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }

        url = "https://echonetwork.app/o/revoke_token/"

        revoke_request = requests.post(url, headers=headers, data=data)

        if refresh:
            data["token"] = refresh
            requests.post(url, headers=headers, data=data)

        if oidc:
            data["token"] = oidc
            requests.post(url, headers=headers, data=data)

        if AccessToken.objects.filter(token=token).exists:
            AccessToken.objects.filter(token=token).delete()

        request.session["active_session"] = None

        data = {
            'message': 'Logged out'
        }

        if not revoke_request.status_code == 200:
            data["message"] = 'Echo Network may have experienced an error. Logged out of Chronicle.'

        return Response(data, status=status.HTTP_200_OK)
    
    else: Response(status=status.HTTP_400_BAD_REQUEST)

@permission_classes([permissions.AllowAny])
@api_view(["POST"])
def intro(request):
    if request.user.is_authenticated:
        data = {
            'user': request.user.username
        }

        return Response(data=data, status=status.HTTP_200_OK)
    else:
        data = {
            'msg': 'NOPE!'
        }

        return Response()
