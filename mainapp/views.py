from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.decorators import authentication_classes, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
import json

# Create your views here.


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def create_new_event(request):
    post_data = json.loads(request.body)
    user_id = request.user.username
    description = post_data['description']
    location = post_data['location']
    address = post_data['address']
    # time should be epoch
    time = post_data['time']
    member_id_list = post_data['members']