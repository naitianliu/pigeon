from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.decorators import authentication_classes, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from contacts.person.person_helper import PersonHelper
from contacts.group.group_helper import GroupHelper
import json

# Create your views here.

"""Person"""


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def person_get_friend_list(request):
    user_id = request.user.username
    obj_person = PersonHelper(user_id)
    friend_info_list = obj_person.get_friend_list()
    return Response(data=friend_info_list, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def person_display_user_list_by_keyword(request):
    user_id = request.user.username
    keyword = request.GET['keyword']
    obj_person = PersonHelper(user_id)
    result_dict = obj_person.display_user_list_by_keyword(keyword)
    return Response(data=result_dict, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def person_send_friend_request(request):
    user_id = request.user.username
    receiver_id = request.GET['receiver_id']
    obj_person = PersonHelper(user_id)
    result_dict = obj_person.send_friend_request(receiver_id)
    return Response(data=result_dict, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def person_get_pending_friend_request_list(request):
    user_id = request.user.username
    obj_person = PersonHelper(user_id)
    result_dict = obj_person.get_pending_friend_request_list()
    return Response(data=result_dict, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def person_accept_friend_request(request):
    user_id = request.user.username
    requester_id = request.GET['requester_id']
    obj_person = PersonHelper(user_id)
    result_dict = obj_person.accept_friend_request(requester_id)
    return Response(data=result_dict, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def person_deny_friend_request(request):
    user_id = request.user.username
    requester_id = request.GET['requester_id']
    obj_person = PersonHelper(user_id)
    result_dict = obj_person.deny_friend_request(requester_id)
    return Response(data=result_dict, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def person_delete_friend(request):
    user_id = request.user.username
    friend_id = request.GET['friend_id']
    obj_person = PersonHelper(user_id)
    result_dict = obj_person.delete_friend(friend_id)
    return Response(data=result_dict, status=status.HTTP_200_OK)


"""Group"""


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def group_get_group_list(request):
    user_id = request.user.username
    obj_group = GroupHelper(user_id)
    group_info_list = obj_group.get_group_list()
    return Response(data=group_info_list, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def group_create_new_group(request):
    user_id = request.user.username
    post_data = json.loads(request.body)
    group_name = post_data['group_name']
    member_list = post_data['members']
    obj_group = GroupHelper(user_id)
    result_dict = obj_group.create_new_group(group_name, member_list)
    return Response(data=result_dict, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def group_edit_group(request):
    user_id = request.user.username
    post_data = json.loads(request.body)
    group_id = post_data['group_id']
    group_name = post_data['group_name']
    member_list = post_data['members']
    obj_group = GroupHelper(user_id)
    result_dict = obj_group.edit_group(group_id, group_name, member_list)
    return Response(data=result_dict, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def group_delete_group(request):
    user_id = request.user.username
    group_id = request.GET['group_id']
    obj_group = GroupHelper(user_id)
    result_dict = obj_group.delete_group(group_id)
    return Response(data=result_dict, status=status.HTTP_200_OK)

