__author__ = 'nliu'

from mainapp.view_set.libs import *
from userinfo.utils.userinfo_helper import UserInfoHelper
from mainapp.utils.notification_helper import NotificationHelper
from mainapp.event.CreateEvent import CreateEventHelper
from mainapp.event.operations.topic import TopicOperation

EVENT_TYPE = "topic"


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def create_topic(request):
    user_id = request.user.username
    post_data = json.loads(request.body)
    topic_name = post_data['topic_name']
    topic_description = post_data['topic_description']
    members = post_data['members']
    event_id = CreateEventHelper(user_id, EVENT_TYPE).create_topic(
        topic_name,
        topic_description,
        members
    )
    device_token_list = UserInfoHelper().get_device_token_list_by_users(members)
    message = topic_name
    payload = dict(
        event_type=EVENT_TYPE,
    )
    NotificationHelper(device_token_list).send_notification_with_payload(message, payload)
    return Response(data=dict(result="success", event_id=event_id), status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def invite_members_to_topic(request):
    user_id = request.user.username
    post_data = json.loads(request.body)
    event_id = post_data['event_id']
    members = post_data['members']
    topic_name = TopicOperation(user_id, event_id).invite_members_to_topic(members)
    return Response(data=dict(result="success"), status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def exit_topic(request):
    user_id = request.user.username
    post_data = json.loads(request.body)
    event_id = post_data['event_id']
    TopicOperation(user_id, event_id).exit_topic()
    return Response(data=dict(result="success"), status=status.HTTP_200_OK)