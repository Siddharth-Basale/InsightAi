import json
from channels.generic.websocket import AsyncWebsocketConsumer

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the room name from the URL route.
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'video_{self.room_name}'

        # Join the room group.
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print(f"WebSocket connected: {self.channel_name} to room {self.room_group_name}")

    async def disconnect(self, close_code):
        # Leave the room group.
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"WebSocket disconnected: {self.channel_name} from room {self.room_group_name}")

    async def receive(self, text_data):
        """
        When a message is received from a client, broadcast it to everyone in the group.
        The client’s JavaScript will handle messages of type "offer", "answer", or "candidate".
        """
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'video_message',
                'message': data,
            }
        )

    async def video_message(self, event):
        """
        Called when a message is sent to the group.
        Forward the message to the WebSocket.
        """
        message = event['message']
        await self.send(text_data=json.dumps(message))