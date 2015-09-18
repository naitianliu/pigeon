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
from mainapp.event.PostHelper import PostHelper
from mainapp.event.CommentHelper import CommentHelper
from userinfo.utils.userinfo_helper import UserInfoHelper
import json

# Create your views here.


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def create_new_event(request):
    try:
        post_data = json.loads(request.body)
        user_id = request.user.username
        description = post_data['description']
        location = post_data['location']
        time = post_data['time']
        member_id_list = post_data['members']
        if user_id not in member_id_list:
            member_id_list.append(user_id)
        event_info = dict(
            creator_id=user_id,
            creator_info=UserInfoHelper().get_user_info(user_id),
            description=description,
            location=location,
            time=time,
            member_id_list=member_id_list,
        )
        EventHelper().create_new_event(event_info, member_id_list)
        return Response(data=dict(result="success"), status=status.HTTP_200_OK)
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


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def create_new_post(request):
    user_id = request.user.username
    post_data = json.loads(request.body)
    event_id = post_data['event_id']
    description = post_data['description']
    img_urls = post_data['img_urls']
    post_info = dict(
        creator_id=user_id,
        description=description,
        event_id=event_id,
        img_urls=img_urls
    )
    PostHelper(user_id).create_new_post(event_id, post_info)
    return Response(data=dict(result="success"), status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def get_post_list(request):
    user_id = request.user.username
    if 'from_time' in request.GET:
        from_time = int(request.GET['from_time'])
    else:
        from_time = None
    if 'to_tome' in request.GET:
        to_time = int(request.GET['to_time'])
    else:
        to_time = None
    if 'event_id' in request.GET:
        event_id = request.GET['event_id']
        post_info_list = PostHelper(user_id).get_post_list_by_event_id(event_id, from_time, to_time)
    else:
        post_info_list = PostHelper(user_id).get_post_list_by_user_id(from_time, to_time)
    return Response(data=post_info_list, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def create_new_comment(request):
    user_id = request.user.username
    post_data = json.loads(request.body)
    post_id = post_data['post_id']
    message = post_data['message']
    img_urls = post_data['img_urls']
    if 'parent_comment_id' in post_data:
        parent_comment_id = post_data['parent_comment_id']
    else:
        parent_comment_id = None
    comment_info = dict(
        creator_id=user_id,
        parent_comment_id=parent_comment_id,
        post_id=post_id,
        message=message,
        img_urls=img_urls
    )
    CommentHelper(user_id).create_new_comment(post_id, comment_info)
    return Response(data=dict(result="success"), status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def get_comment_list(request):
    user_id = request.user.username
    if 'from_time' in request.GET:
        from_time = int(request.GET['from_time'])
    else:
        from_time = None
    if 'to_tome' in request.GET:
        to_time = int(request.GET['to_time'])
    else:
        to_time = None
    post_id = request.GET['post_id']
    comment_info_list = CommentHelper(user_id).get_comment_list_by_post_id(post_id, from_time, to_time)
    return Response(data=comment_info_list, status=status.HTTP_200_OK)