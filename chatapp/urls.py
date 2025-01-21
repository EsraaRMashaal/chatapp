from django.urls import path
from . import views

urlpatterns = [
    path("create-room/", views.create_room, name="create_room"),
    path("rooms/", views.get_rooms, name="get_rooms"),
    path("delete-room/<int:room_id>/", views.delete_room, name="delete_room"), 
    path("send-message/", views.send_message, name="send_message"),
]
