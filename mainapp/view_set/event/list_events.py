__author__ = 'nliu'

from mainapp.view_set.libs import *
from mainapp.event.get.list_events import ListEventsHelper


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def get_all_updated_events_list(request):
    user_id = request.user.username
    event_info_list = ListEventsHelper(user_id).get_all_updated_events_list()
    return Response(data=dict(result=event_info_list), status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((BasicAuthentication, TokenAuthentication))
@permission_classes((IsAuthenticated,))
def get_event_info(request):
    user_id = request.user.username
    event_id = request.GET['event_id']
    event_info = ListEventsHelper(user_id).get_event_info(event_id)
    return Response(data=event_info, status=status.HTTP_200_OK)