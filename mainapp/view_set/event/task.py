__author__ = 'nliu'

from mainapp.view_set.libs import *
from userinfo.utils.userinfo_helper import UserInfoHelper
from mainapp.utils.notification_helper import NotificationHelper
from mainapp.event.CreateEvent import CreateEventHelper
from mainapp.event.operations.task import TaskOperation

EVENT_TYPE = "task"


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def create_task(request):
    user_id = request.user.username
    post_data = json.loads(request.body)
    task_name = post_data['task_name']
    task_description = post_data['task_description']
    todo_list = post_data['todo_list']
    members = post_data['members']
    time_dict = post_data['time']
    location_dict = post_data['location']
    event_id = CreateEventHelper(user_id, EVENT_TYPE).create_task(
        task_name,
        task_description,
        todo_list,
        members,
        time_dict,
        location_dict
    )
    device_token_list = UserInfoHelper().get_device_token_list_by_users(members)
    message = task_name
    payload = dict(
        event_type=EVENT_TYPE,
    )
    NotificationHelper(device_token_list).send_notification_with_payload(message, payload)
    return Response(data=dict(result="success", event_id=event_id), status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def invite_members_to_task(request):
    user_id = request.user.username
    post_data = json.loads(request.body)
    event_id = post_data['event_id']
    members = post_data['members']
    task_name = TaskOperation(user_id, event_id).invite_members_to_task(members)
    device_token_list = UserInfoHelper().get_device_token_list_by_users(members)
    message = task_name
    payload = dict(
        event_type=EVENT_TYPE,
    )
    NotificationHelper(device_token_list).send_notification_with_payload(message, payload)
    return Response(data=dict(result="success"), status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def accept_task(request):
    user_id = request.user.username
    post_data = json.loads(request.body)
    event_id = post_data['event_id']
    if 'message' in post_data:
        message = post_data
    else:
        message = None
    TaskOperation(user_id, event_id).accept_task(message=message)
    return Response(data=dict(result="success"), status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def reject_task(request):
    user_id = request.user.username
    post_data = json.loads(request.body)
    event_id = post_data['event_id']
    if 'message' in post_data:
        message = post_data
    else:
        message = None
    TaskOperation(user_id, event_id).reject_task(message=message)
    return Response(data=dict(result="success"), status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def exit_task(request):
    user_id = request.user.username
    post_data = json.loads(request.body)
    event_id = post_data['event_id']
    if 'message' in post_data:
        message = post_data
    else:
        message = None
    TaskOperation(user_id, event_id).exit_task(message=message)
    return Response(data=dict(result="success"), status=status.HTTP_200_OK)



