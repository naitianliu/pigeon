__author__ = 'nliu'

from mainapp.view_set.libs import *
from userinfo.utils.userinfo_helper import UserInfoHelper
from mainapp.utils.notification_helper import NotificationHelper
from mainapp.event.CreateEvent import CreateEventHelper
from mainapp.event.operations.reminder import ReminderOperation

EVENT_TYPE = "reminder"


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def create_reminder(request):
    user_id = request.user.username
    post_data = json.loads(request.body)
    reminder_content = post_data['reminder_content']
    receivers = post_data['receivers']
    time_dict = post_data['time']
    location_dict = post_data['location']
    event_id = CreateEventHelper(user_id, EVENT_TYPE).create_reminder(
        reminder_content,
        receivers,
        time_dict,
        location_dict
    )
    device_token_list = UserInfoHelper().get_device_token_list_by_users(receivers)
    message = reminder_content
    payload = dict(
        event_type=EVENT_TYPE,
    )
    NotificationHelper(device_token_list).send_notification_with_payload(message, payload)
    return Response(data=dict(result="success", event_id=event_id), status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def change_receivers(request):
    user_id = request.user.username
    post_data = json.loads(request.body)
    event_id = post_data['event_id']
    receivers = post_data['receivers']
    ReminderOperation(user_id, event_id).change_receivers(receivers)
    return Response(data=dict(result="success"), status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def complete_reminder_by_receiver(request):
    user_id = request.user.username
    post_data = json.loads(request.body)
    event_id = post_data['event_id']
    if 'message' in post_data:
        message = post_data['message']
    else:
        message = None
    creator_id = ReminderOperation(user_id, event_id).complete_reminder_by_receiver(message)
    device_token_list = UserInfoHelper().get_device_token_list_by_users([creator_id])
    message = "complete"
    payload = dict(
        event_type=EVENT_TYPE,
    )
    NotificationHelper(device_token_list).send_notification_with_payload(message, payload)
    return Response(data=dict(result="success"), status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def revoke_reminder_by_creator(request):
    user_id = request.user.username
    post_data = json.loads(request.body)
    event_id = post_data['event_id']
    if 'message' in post_data:
        message = post_data['message']
    else:
        message = None
    ReminderOperation(user_id, event_id).revoke_reminder_by_creator(message)
    return Response(data=dict(result="success"), status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def delay_reminder_by_receiver(request):
    user_id = request.user.username
    post_data = json.loads(request.body)
    event_id = post_data['event_id']
    if 'message' in post_data:
        message = post_data['message']
    else:
        message = None
    ReminderOperation(user_id, event_id).delay_reminder_by_receiver(message)
    return Response(data=dict(result="success"), status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def reject_reminder_by_receiver(request):
    user_id = request.user.username
    post_data = json.loads(request.body)
    event_id = post_data['event_id']
    if 'message' in post_data:
        message = post_data['message']
    else:
        message = None
    ReminderOperation(user_id, event_id).reject_reminder_by_receiver(message)
    return Response(data=dict(result="success"), status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def resend_reminder_by_creator(request):
    user_id = request.user.username
    post_data = json.loads(request.body)
    event_id = post_data['event_id']
    if 'message' in post_data:
        message = post_data['message']
    else:
        message = None
    ReminderOperation(user_id, event_id).resend_reminder_by_creator(message)
    return Response(data=dict(result="success"), status=status.HTTP_200_OK)