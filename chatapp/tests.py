from django.test import TestCase, Client
from django.urls import reverse
from chatapp.models import CustomUser, ChatRoom, Message

class ChatAppTestCase(TestCase):
    def setUp(self):
        # creat a user 
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@gmail.com",
            password="testpassword"
        )

        # create a chat room
        self.chat_room = ChatRoom.objects.create(
            name="Test Room"
        )

        # add participants to the chat room
        self.chat_room.participants.add(self.user)

    def test_get_rooms(self):
        client = Client()
        response = client.get(reverse("get_rooms"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chatapp/rooms.html")
        self.assertContains(response, "Test Room")

    def test_delete_room(self):
        client = Client()
        client.login(username="testuser", password="testpassword")
        response = client.post(reverse("delete_room", args=[self.chat_room.id]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ChatRoom.objects.count(), 0)

    def test_send_message(self):
        client = Client()
        client.login(username="testuser", password="testpassword")
        response = client.post(reverse("send_message"), {
            "chat_room_id": self.chat_room.id,
            "sender_id": self.user.id,
            "text": "Hello, how are you?"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.first().text, "Hello, how are you?")



