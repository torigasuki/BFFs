from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Alarm


class AlarmView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, alarm_id=None):
        if alarm_id is not None:
            alarm = Alarm.objects.get(id=alarm_id)
        else:
            alarm = Alarm.objects.filter(user=request.user)
        alarm.delete()
        return Response({"message": "알람이 삭제되었습니다"}, status=status.HTTP_200_OK)
