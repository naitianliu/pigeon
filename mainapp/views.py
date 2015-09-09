from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.decorators import authentication_classes, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from userinfo.utils.userinfo_helper import UserInfoHelper
from mainapp.event.EventHelper import EventHelper
import json

# Create your views here.


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def create_new_event(request):
    try:
        post_data = json.loads(request.body)
        print(post_data)
        user_id = request.user.username
        description = post_data['description']
        location = post_data['location']
        address = post_data['address']
        time = post_data['time']
        member_id_list = post_data['members']
        event_info = dict(
            creator_id=user_id,
            description=description,
            location=location,
            address=address,
            time=time,
            member_id_list=member_id_list,
        )
        print(1)
        EventHelper().create_new_event(event_info, member_id_list)
        print(2)
        return Response(data=dict(result="success"), status=status.HTTP_204_NO_CONTENT)
    except Exception as err:
        print(err)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def get_event_list(request):
    user_id = request.user.username
    if 'from_time' in request.GET:
        from_time = int(request.GET['from_time'])
    else:
        from_time = None
    if 'to_tome' in request.GET:
        to_time = int(request.GET['to_time'])
    else:
        to_time = None
    event_info_list = EventHelper().get_event_list_by_user_id(user_id, from_time=from_time, to_time=to_time)
    return Response(data=event_info_list, status=status.HTTP_200_OK)