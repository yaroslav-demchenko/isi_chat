from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Thread, Message
from .serializers import ThreadSerializer, MessageSerializer


@api_view(["POST", "DELETE", "GET"])
def create_thread(request):
    if request.method == "GET":
        threads = Thread.objects.filter(participants=request.user.id)
        serializer = ThreadSerializer(threads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    participants_id = request.data.get("participants", [])
    if len(participants_id) != 2:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    thread = Thread.objects.filter(participants=participants_id[0]).filter(
        participants=participants_id[1]
    )

    if request.method == "POST":
        if thread:
            serializer = ThreadSerializer(thread.get())
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = ThreadSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == "DELETE":
        thread.get().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        thread_id = self.kwargs["thread_id"]
        return Message.objects.filter(thread_id=thread_id)

    def perform_create(self, serializer):
        thread_id = self.kwargs["thread_id"]
        thread = get_object_or_404(Thread, pk=thread_id)
        serializer.save(sender=self.request.user, thread=thread)


@api_view(["GET"])
def unread_messages_count(request):
    count = Message.objects.filter(
        thread__participants=request.user, is_read=False
    ).count()
    return Response({"count": count}, status=status.HTTP_200_OK)


@api_view(["POST"])
def mark_message_as_read(request, message_id):
    try:
        message = Message.objects.get(id=message_id, thread__participants=request.user)
    except Message.DoesNotExist:
        return Response(
            {"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND
        )

    message.is_read = True
    message.save()

    return Response({"message": "Message marked as read"}, status=status.HTTP_200_OK)
