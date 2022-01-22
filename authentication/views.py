from django.template import exceptions
from rest_framework.response import Response
from rest_framework import status, generics, views
from authentication.serializers import (EmailVerifySerializer, LoginSerializer,
                                         RegisterSerializer, RequestPasswordResetEmailSerializer,
                                         SetPasswordSerializer
                                         )
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
from django.utils.encoding import smart_bytes, smart_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator



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
    using swagger docs set up the configuration as stated below
    
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
"""
Steps for setting up password reset

Setup an email view so as to send an email containing the link to set email
View that when a user clicks a link in  the email the browser does a get request to validate the links
Set up a view that sets up the password


"""

class RequestPasswordResetEmailApiView(generics.GenericAPIView):
        serializer_class = RequestPasswordResetEmailSerializer
        def post(self, request):
            serializer = self.serializer_class(data=request.data)
            data=request.data
            
            """
                A function that gets called when is_valid() is invoked
                We get the user and create a uid64 for the user, then make a password reset token for the user
                Using the sites framework, a url is created with the users data and using the send_mail function in the
                util module , send an email to the user

                from django.utils.encording

                smart_str(s, encoding='utf-8', strings_only=False, errors='strict')
                Returns a str object representing arbitrary object s. Treats bytestrings using the encoding codec.

                force_str(s, encoding='utf-8', strings_only=False, errors='strict')
                Similar to smart_str(), except that lazy instances are resolved to strings, rather than kept as lazy objects.


                smart_bytes(s, encoding='utf-8', strings_only=False, errors='strict')
                Returns a bytestring version of arbitrary object s, encoded as specified in encoding.

            

                force_bytes(s, encoding='utf-8', strings_only=False, errors='strict')
                Similar to smart_bytes, except that lazy instances are resolved to bytestrings, rather than kept as lazy objects.



                from django.utils.http
                urlsafe_base64_encode(s)
                    Encodes a bytestring to a base64 string for use in URLs, stripping any trailing equal signs.

                urlsafe_base64_decode(s)
                Decodes a base64 encoded string, adding back any trailing equal signs that might have been stripped.
            """
            email = data.get("email", "")
            if CustomUser.objects.filter(email=email).exists():
                user = CustomUser.objects.get(email=email)
                uid64 = urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)

                relative_link = reverse("password-reset-email", kwargs={'uidb64':uid64, 'token': token})
                
                """
                get_current_site() function will try to get the current site by comparing the domain with the host name from the request.get_host() method.
                
                """
                current = get_current_site(request).domain
                abs_url = f"http://{current}{relative_link}"
                email_body = f""" Hello . Click the link below to activate your email\n{abs_url}        
                                """
                data = {
                    "email_body": email_body,
                    "subject": "Password Reset",
                    "to_email": user.email
                }
                Util.send_mail(data)
            return Response({"Success": "We have sent you a link to reset your pasword"}, status=status.HTTP_200_OK)



class TokenCheckApi(generics.GenericAPIView):

        """
        View that when a user clicks a link in  the email the browser does a get request 
        to validate the links

        """

        def get(self, request, uidb64, token):

            """
            get the user's id based on the uidb64
            
            """
            try:
                id = smart_str(urlsafe_base64_decode(uidb64))
                user = CustomUser.objects.get(id=id)
                """"
                check tokens that have not been tampered with by the user
                """

                if not PasswordResetTokenGenerator().check_token(user, token):
                    return Response({"error": "bad credentials or the has already been used"})
                return Response({"success": True, "message": "credentials valid", "uidb64": uidb64, "token": token})




            except UnicodeDecodeError as e:
                return Response({"error": "Token is not valid. Pease request another one"})

class SetPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetPasswordSerializer
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"success": True, "Message": "Password reset successfully"}, status = status.HTTP_200_OK)
