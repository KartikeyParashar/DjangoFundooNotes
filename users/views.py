"""
******************************************************************************************************************
Purpose: In this views module, I created a rest_api for register, reset_password, forgot_password,
         social_login through Google OAuth, image_upload in AWS S3 Bucket
Author:  KARTIKEY PARASHAR
Since :  20-02-2020
******************************************************************************************************************
"""
import json
import jwt
import requests
import logging
from urllib.parse import unquote

from django.contrib import messages
from django.http import HttpResponse
from django_short_url.views import get_surl
from django_short_url.models import ShortURL
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model, authenticate, logout

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from FUNDOONOTES import settings
from Lib import redis_cache
from Lib.user_detail import get_user
from Lib.aws_service import CloudUpload
from Lib.decorators import login_required
from Lib.smd_response import SMD_Response
from Lib.event_emmiter import email_event
from Lib.pyjwt_token import TokenGeneration

from .models import Fundoo
from .serializers import RegistrationSerializer, LoginSerializer, \
    ResetPasswordSerializer, ForgotPasswordSerializer, ImageSerializer, PhoneSerializer

logger = logging.getLogger(__name__)


class RegistrationAPIView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        :purpose: in this function we register a new user via sending jwt token on email
        :param request: here we get post request
        :return:in this function we take user input for registration and sent mail to email id
        """
        try:
            # import pdb
            # pdb.set_trace()
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']
            if password != '':
                User = get_user_model()
                if User.objects.filter(username=username).exists():
                    messages.info(request, "Username Already Exists")
                    smd = SMD_Response(message="Username Already Exists!!Please enter a different username")
                    return Response(smd, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    token = TokenGeneration.encode_token(self, user)
                    surl = get_surl(token)
                    url = surl.split("/")
                    message = render_to_string('users/activate.html',
                                               {'user': user.username,
                                                'domain': get_current_site(request).domain,
                                                'token': url[2]})
                    recipient_list = [email, ]
                    email_event.emit("Account_Activate_Event", message, recipient_list)
                    smd = SMD_Response(True, 'Thank You For Registering to our site, '
                                             'Please check mail to activate your account', data=[])
                    return Response(smd, status=201)
            else:
                smd = SMD_Response(message="Password is Not Correct")
                return Response(smd, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Something Went Wrong" + str(e))
            smd = SMD_Response(message="Registration Failed")
            return Response(smd, status=status.HTTP_400_BAD_REQUEST)


def activate(request, token):
    """
    :param request: here we use get request
    :param token:here we get token
    :return:in this function we get token when user click the link and we decode the token and
            activate the user
    """
    try:
        import pdb
        # pdb.set_trace()
        token1 = ShortURL.objects.get(surl=token)
        token = token1.lurl
        details = TokenGeneration.decode_token(token)
        username = details['username']
        User = get_user_model()
        user = User.objects.get(username=username)
        if user is not None:
            user.is_active = True
            user.save()
            # smd = SMD_Response(True, "You have successfully registered", data=[])
            return redirect(reverse('login'))
        else:
            return redirect(reverse('register'))
    except Exception as e:
        logger.error("Something Went Wrong" + str(e))
        smd = SMD_Response(False, "Invalid Token Received", data=[])
        return HttpResponse(json.dumps(smd), status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        """
        :param request: Here we get the post request
        :return:This api view return token of the logged in user
        """
        try:
            # import pdb
            # pdb.set_trace()
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user != '':
                token = TokenGeneration.encode_token(self, user)
                Token = 'Token'
                redis_cache.Set(Token, token)
                smd = SMD_Response(True, "You have Logged in successfully!!!", data=[token])
                return Response(smd, status=status.HTTP_202_ACCEPTED)
            else:
                smd = SMD_Response(False, "Please Enter Valid Credentials", data=[])
                return Response(smd, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error("Something Went Wrong" + str(e))
            smd = SMD_Response(False, "Login Failed!!!", data=[])
            return Response(smd, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        """
        :param request: here is post request por set password
        :return: in this function we take email from user and send token for verification
        """
        try:
            username = request.data['username']
            email = request.data['email']
            User = get_user_model()
            user = User.objects.get(username=username, email=email)
            if user:
                payload = {
                    'username': user.username,
                    'email': user.email
                }
                token = jwt.encode(payload, 'SECRET_KEY', algorithm='HS256').decode('utf-8')
                surl = get_surl(token)
                url = surl.split('/')
                message = render_to_string('users/reset_password.html',
                                           {
                                               'user': user.username,
                                               'domain': get_current_site(request).domain,
                                               'token': url[2]
                                           })
                recipient_list = [email, ]
                email_event.emit("Reset_Password_Event", message, recipient_list)
                smd = SMD_Response(True, 'We have sent an email, '
                                         'please click there on link to reset password', data=[])
                return Response(smd, status=status.HTTP_200_OK)

            else:
                smd = SMD_Response(False, 'Reset Password Process Failed', data=[])
                return Response(smd, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Something Went Wrong" + str(e))
            smd = SMD_Response(status=False, message="Failed!!!")
            return Response(smd, status=status.HTTP_400_BAD_REQUEST)


def verify(request, token):
    """
    :param request: request for reset password
    :param token: here we get token for decoding that the user details, who wants to change the password
    :return:this function redirect to the user's forgot password page
    """
    try:
        token1 = ShortURL.objects.get(surl=token)
        token = token1.lurl
        details = jwt.decode(token, 'SECRET_KEY', algorithm='HS256')
        username = details['username']
        User = get_user_model()
        user = User.objects.get(username=username)
        if user:
            user.save()
            return redirect(reverse('forgot_password', args=[str(user)]))
        else:
            smd = SMD_Response(message="User Does Not Exist")
            return HttpResponse(smd, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error("Something Went Wrong" + str(e))
        smd = SMD_Response(message="Invalid Details!!!Verification Failed!!!")
        return HttpResponse(smd, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordAPIView(GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request, ResetUser):
        """
        :param request: Here we get the post request
        :param ResetUser: It is the user who wants to reset the password
        :return: Successfully change the password and save it in the DATABASE
        """
        try:
            User = get_user_model()
            user = User.objects.get(username=ResetUser)
            if user:
                password = request.data['password']
                confirm_password = request.data['confirm_password']
                if password == confirm_password:
                    user.set_password(password)
                    user.save()
                    smd = SMD_Response(status=True, message="Password Set SuccessFully")
                    return Response(smd, status=status.HTTP_200_OK)
                else:
                    smd = SMD_Response(message="Password and Confirm Password did not match")
                    return Response(smd, status=status.HTTP_400_BAD_REQUEST)
            else:
                smd = SMD_Response(status=False, message="User does not exist!!!")
                return Response(smd, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error("Something Went Wrong" + str(e))
            smd = SMD_Response(status=False, message="Reset Password Failed!!!")
            return Response(smd, status=status.HTTP_400_BAD_REQUEST)


class Logout(GenericAPIView):

    @method_decorator(login_required, name='dispatch')
    def get(self, request, *args, **kwargs):
        """
        :param request: Here we got the GET request
        :return: It will logout the Logged In user
        """
        # import pdb
        # pdb.set_trace()
        try:
            redis_cache.Del('Token')
            logout(request)
            smd = SMD_Response(status=True, message="Successfully Logged Out")
            return Response(smd, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Something Went Wrong" + str(e))
            smd = SMD_Response(message="Logged Out Failed")
            return Response(smd, status=status.HTTP_400_BAD_REQUEST)


class UploadImage(GenericAPIView):
    serializer_class = ImageSerializer

    def post(self, request):
        """
        :param-Here image is using for uploading into the AWS s3-bucket
        :request-by using Secret Key and Bucket Storage name uploading the image into the S3-Bucket
        :return-successfully image uploaded into the S3-Bucket
        """
        try:
            # import pdb
            # pdb.set_trace()
            serializer = ImageSerializer(data=request.data)
            if serializer.is_valid():
                user = get_user(request)
                exist_image = Fundoo.objects.get(id=user.id)
                if exist_image:
                    filee = request.data['upload']
                    up = CloudUpload()
                    url = f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3-{settings.AWS_LOCATION}.amazonaws.com/{filee}'
                    up.upload_image(filee)
                    exist_image.upload = url
                    exist_image.save()
                    smd = SMD_Response(status=True, message="Successfully Uploaded Image to S3 BUCKET."
                                                            "Please go to your AWS Account and "
                                                            "see image in your bucket having url")
            else:
                smd = SMD_Response(message="Please Enter a Valid Image",
                                   status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        except Exception as e:
            logger.error("Something Went Wrong" + str(e))
            smd = SMD_Response(message="something went wrong, Image not uploaded successfully...")
        return Response(json.dumps(smd))


class SimpleNotificationService(GenericAPIView):
    serializer_class = PhoneSerializer

    def post(self, request):
        """

        :param request: we are sending text message to the user
        :return: successfully send message to the user
        """
        try:
            serializer = PhoneSerializer(data=request.data)
            if serializer.is_valid():
                send = CloudUpload()
                send.simple_notification_service(request.data['phone'])
                return Response(SMD_Response(status=True, message="Successfully send message",
                                             data=[serializer.data]),
                                status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Something Went Wrong" + str(e))
            smd = SMD_Response(message="Something Went Wrong")
            return Response(smd, status=status.HTTP_400_BAD_REQUEST)


class SocialLogin(GenericAPIView):
    def get(self, request):
        """

        :param request: here we get code from google oauth2
        :return:in this function by using the code from the google, we get access token,
                and by using that token we get user information after that we get email id of that user
                and redirect that user to HOMEPAGE
        """
        return render(request, 'users/social_login.html')


def access_token(request):
    """
    :param request: here we get code from google oauth2
    :return:in this function by using the code from the google, we get access token,
            and by using that token we get user information after that we get email id of that user
            and redirect that user to HOMEPAGE
    """
    try:
        # import pdb
        # pdb.set_trace()
        path = request.get_full_path()
        code_path = path.split('&')
        code = code_path[1].split('=')
        code = unquote(code[1])
        # print(code)

        url = settings.GOOGLE_ACCESS_TOKEN_URI
        data = {
            "code": code,
            "client_id": settings.GOOGLE_OAUTH2_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH2_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "redirect_uri": settings.GOOGLE_REDIRECT_URI
        }
        response = requests.post(url, data)
        token = json.loads(response.text)['access_token']
        headers = {'Authorization': 'OAuth %s' % token}
        req = requests.get(settings.SOCIAL_AUTH_GET_GOOGLE_INFO, headers=headers)
        google_data = req.json()
        email_address = google_data['emailAddress']
        if email_address is not None:
            return redirect(settings.BASE_URL)
        else:
            smd = SMD_Response(message='Email Address is not Valid')
    except Exception as e:
        logger.error("Something Went Wrong" + str(e))
        smd = SMD_Response()
    return smd



