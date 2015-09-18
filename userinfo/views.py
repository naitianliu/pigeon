from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.decorators import authentication_classes, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from userinfo.utils.register import UserRegisterHelper
from userinfo.utils.vendor_login import VendorLogin
from django.contrib.auth.models import User as django_user
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
import json

# Create your views here.


def user(request):
    return HttpResponse("user api")


def test(request):
    from mainapp.utils.notification_helper import NotificationHelper
    device_token = "2F79378100B67B4CABB83F03AE52493120D73B6F0BE848FE3899BFCCE49A4352"
    message = "hello!"
    button_title = "Confirm"
    NotificationHelper(device_token).send_notification_with_custome_button(message, button_title)
    return HttpResponse(json.dumps(dict(result="OK")), content_type="application/json")


@csrf_exempt
def user_register(request):
    try:
        post_data = json.loads(request.body)
        vendor_id = post_data['vendor_id']
        vendor_type = post_data['vendor_type']
        if vendor_type == "email":
            password = post_data['password']
            UserRegisterHelper().register_new_user_by_email(vendor_id, vendor_type, password)
        res_data = dict(
            result="success"
        )
        return HttpResponse(json.dumps(res_data), content_type="application/json")
    except Exception as err:
        print(err)


@csrf_exempt
def verify_passcode(request):
    post_data = json.loads(request.body)
    user_id = post_data['user_id']
    passcode = post_data['passcode']
    is_valid = UserRegisterHelper().verify_passcode(user_id, passcode)
    print(is_valid)
    if is_valid:
        user = django_user.objects.get(username=user_id)
        user.backend = "django.contrib.auth.backends.ModelBackend"
        auth.login(request, user)
        print(request)
        token = request.session.session_key
        res_data = dict(
            result="success",
            token=token
        )
    else:
        res_data = dict(
            result="failure"
        )
    return HttpResponse(json.dumps(res_data), content_type="application/json")


@csrf_exempt
def login(request):
    post_data = json.loads(request.body)
    user_id = post_data['user_id']
    password = post_data['password']
    user_obj = authenticate(username=user_id, password=password)
    if user_obj:
        if user_obj.is_active:
            user = django_user.objects.get(username=user_id)
            user.backend = "django.contrib.auth.backends.ModelBackend"
            auth.login(request, user)
            message = "logged in"
            res_data = dict(
                result="success",
                message=message,
                #token=request.session.session_key
                token=Token.objects.get_or_create(user=user)[0].key
            )
        else:
            message = "inactive user"
            res_data = dict(
                result="failure",
                message=message
            )
    else:
        message = "invalid username or password"
        res_data = dict(
            result="failure",
            message=message
        )
    print(res_data)
    return HttpResponse(json.dumps(res_data), content_type="application/json")


def logout(request):
    auth.logout(request)
    res_data = dict(
        result="success"
    )
    return HttpResponse(json.dumps(res_data), content_type="application/json")


def check_existing_user_id(request):
    vendor_id = request.GET['vendor_id']
    vendor_type = request.GET['vendor_type']


def resend_validation_passcode(request):
    pass



@api_view(['GET'])
def vendor_login(request):
    print(1)
    vendor_type = request.GET['vendor_type']
    vendor_id = request.GET['vendor_id']
    access_token = request.GET['access_token']
    try:
        user_id = VendorLogin(vendor_type, vendor_id, access_token).login()
    except Exception as err:
        print err
    print(user_id)
    if user_id:
        try:
            user = django_user.objects.get(username=user_id)
        except django_user.DoesNotExist:
            user = django_user.objects.create_user(username=user_id)
        user.backend = "django.contrib.auth.backends.ModelBackend"
        auth.login(request, user)
        print(1)
        token = Token.objects.get_or_create(user=user)[0].key
        print(2)
        data = dict(
            token=token
        )
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)