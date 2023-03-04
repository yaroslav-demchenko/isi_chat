from rest_framework import serializers
from chat.models import Thread, Message


class ThreadSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ["id", "participants", "created", "updated", "last_message"]

    def get_last_message(self, obj):
        last_message = obj.messages.order_by("-created").first()
        if last_message:
            return {
                "id": last_message.id,
                "sender": last_message.sender.username,
                "text": last_message.text,
                "created": last_message.created,
                "is_read": last_message.is_read,
            }
        return None


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source="sender.username")

    class Meta:
        model = Message
        fields = ["id", "sender", "text", "thread", "created", "is_read"]
