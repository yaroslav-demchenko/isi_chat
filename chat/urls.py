from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    create_thread,
    delete_thread,
    MessageListCreateAPIView,
    unread_messages_count,
    mark_message_as_read,
)

app_name = "myapp"

urlpatterns = [
    path("threads/", create_thread, name="create_thread"),
    path("threads/<int:thread_id>/", delete_thread, name="delete_thread"),
    path(
        "threads/<int:thread_id>/messages/",
        MessageListCreateAPIView.as_view(),
        name="message_list_create",
    ),
    path(
        "messages/<int:message_id>/mark_as_read/",
        mark_message_as_read,
        name="mark_message_as_read",
    ),
    path("unread_messages_count/", unread_messages_count, name="unread_messages_count"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
