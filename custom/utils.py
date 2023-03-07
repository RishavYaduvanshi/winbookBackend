from asgiref.sync import sync_to_async
from rest_framework.serializers import ModelSerializer


@sync_to_async
def saveSerializer(serializer: ModelSerializer):
    serializer.is_valid(raise_exception=True)
    serializer.save()
    # serializer.instance.send_message()
