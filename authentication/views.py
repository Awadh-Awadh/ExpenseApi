from rest_framework.response import Response
from rest_framework import status, generics, views
from authentication.serializers import EmailVerifySerializer, LoginSerializer, RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from .renderers import AuthRender



# Create your views here.


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    renderer_classes = (AuthRender,)

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data

            "Creating tokens Manually"
            user = CustomUser.objects.get(email=user_data['email'])
            token = RefreshToken.for_user(user).access_token

            #using sites framework to create domains that users click for email verification

            current_site = get_current_site(request).domain
            relative_link = reverse('verify-email')
            absurl = f'http://{current_site}{relative_link}?token={str(token)}'
            email_body = f"""            
            Hello {user_data['username']}. Click the link below to activate your email\n            
            {absurl}        
            """

            data = {
                "email_body": email_body,
                "subject": "Verify your email",
                "to_email": user.email
            }
            '''
            sending email that contains all email verification link
            '''
            Util.send_mail(data)

            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class VerifyEmail(views.APIView):
    '''
    Manually creating token description fields in the swager ui
    
    '''
    token_param = openapi.Parameter('token', in_=openapi.IN_QUERY, description="Description", type=openapi.TYPE_STRING)
    serializer_class = EmailVerifySerializer
    @swagger_auto_schema(manual_parameters=[token_param])    
    def get(self, request):
        token = request.GET.get('token')
        try:
            decorded = jwt.decode(token, settings.SECRET_KEY)
            user = CustomUser.objects.get(id=decorded['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'email is successfully verified'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'Error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({"error": "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)
            


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(username=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials. Try again")

        if not user.is_active:
            raise AuthenticationFailed("Account disabled contact admin")

        if user.is_verified:
            raise AuthenticationFailed("Email is not verified")

        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


        