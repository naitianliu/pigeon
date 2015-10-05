__author__ = 'nliu'

from mainapp.view_set.libs import *
from userinfo.utils.userinfo_helper import UserInfoHelper
from mainapp.utils.notification_helper import NotificationHelper
from mainapp.event.CreateEvent import CreateEventHelper
from mainapp.event.operations.activity import ActivityOperation

EVENT_TYPE = "activity"


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def create_activity(request):
    user_id = request.user.username
    post_data = json.loads(request.body)
    activity_description = post_data['activity_description']
    members = post_data['members']
    time_dict = post_data['time']
    location_dict = post_data['location']
    event_id = CreateEventHelper(user_id, EVENT_TYPE).create_activity(
        activity_description,
        members,
        time_dict,
        location_dict
    )
    device_token_list = UserInfoHelper().get_device_token_list_by_users(members)
    message = activity_description
    payload = dict(
        event_type=EVENT_TYPE,
    )
    NotificationHelper(device_token_list).send_notification_with_payload(message, payload)
    return Response(data=dict(result="success", event_id=event_id), status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def invite_members_to_activity(request):
    user_id = request.user.username
    post_data = json.loads(request.body)
    event_id = post_data['event_id']
    members = post_data['members']
    ActivityOperation(user_id, event_id).invite_members_to_activity(members)
    device_token_list = UserInfoHelper().get_device_token_list_by_users(members)
    message = "activity"
    payload = dict(
        event_type=EVENT_TYPE,
    )
    NotificationHelper(device_token_list).send_notification_with_payload(message, payload)
    return Response(data=dict(result="success"), status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def exit_activity(request):
    user_id = request.user.username
    post_data = json.loads(request.body)
    event_id = post_data['event_id']
    ActivityOperation(user_id, event_id).exit_topic()
    return Response(data=dict(result="success"), status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def post_notification(request):
    user_id = request.user.username
    post_data = json.loads(request.body)
    event_id = post_data['event_id']
    notification_content = post_data['notification_content']
    members = ActivityOperation(user_id, event_id).post_notification(notification_content)
    device_token_list = UserInfoHelper().get_device_token_list_by_users(members)
    message = notification_content
    payload = dict(
        event_type=EVENT_TYPE,
    )
    NotificationHelper(device_token_list).send_notification_with_payload(message, payload)
    return Response(data=dict(result="success"), status=status.HTTP_200_OK)