from rest_framework.response import Response
from rest_framework import status, generics
from authentication.serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

# Create your views here.


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data

            "Creating tokens Manually"
            user = CustomUser.objects.get(email=user_data['email'])
            token = RefreshToken.for_user(user).access_token

            #using sites framework to create domains
            current_site = get_current_site(request).domain
            relative_link = reverse('verify-email')
            absurl = 'http://' +current_site + relative_link + '?token='+str(token)
            email_body = f"""            
            Hello {user_data['username']}. Click the link below to activate your email\n            
            {absurl}        
            """

            data = {
                "email_body": email_body,
                "subject": "Verify your email",
                "to_email": user.email
            }

            Util.send_mail(data)

            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        ...