from django.shortcuts import render, redirect, get_object_or_404
from .models import ChatRoom, Message, CustomUser
from django.contrib import messages

"""
The `create_room` view function is used to create a new chat room. 
"""
def create_room(request):
    if request.method == "POST":
        name = request.POST.get("name")
        participants = request.POST.getlist("participants")

        if not name:
            message = "Please provide a name for the chat room."
            messages.error(request, message)
            return redirect("create_room")
        
        if not participants:
            message = "Please select participants for the chat room."
            messages.error(request, message)
            return redirect("create_room")



        new_room = ChatRoom.objects.create(name=name)
        new_room.participants.set(participants)

        message = "Chat room created successfully."
        messages.success(request, message)
        return redirect("get_rooms")

    return render(request, "chatapp/create_room.html", {"new_room": new_room})
    

"""
The `get_rooms` view function is used to get all chat rooms.
"""
def get_rooms(request):
    all_rooms = ChatRoom.objects.all()
    return render(request, "chatapp/rooms.html", {"rooms": all_rooms})


"""
The `room_messages` view function is used to get all messages in a chat room.
"""
def delete_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    room.delete()

    message = "Chat room deleted successfully."
    messages.success(request, message)
    return redirect("get_rooms")

"""
The `room_messages` view function is used to get all messages in a chat room.
"""
def send_message(request):
    if request.method == "POST":
        chat_room_id = request.POST.get("chat_room_id")
        sender_id = request.POST.get("sender_id")
        text = request.POST.get("text")    

        if not chat_room_id:
            message = "Please provide a chat room ID."
            messages.error(request, message)
            return redirect("send_message")
        
        if not sender_id:
            message = "Please provide a sender ID."
            messages.error(request, message)
            return redirect("send_message")
        
        if not text:
            message = "Please provide a message."
            messages.error(request, message)
            return redirect("send_message")

        chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
        sender = get_object_or_404(CustomUser, id=sender_id)
        new_message = Message.objects.create(chat_room=chat_room, sender=sender, text=text)

        message = "Message sent successfully."
        messages.success(request, message)
        return redirect("room_messages", chat_room_id=chat_room_id, message_id=new_message.id)

    return render(request, "chatapp/send_message.html")