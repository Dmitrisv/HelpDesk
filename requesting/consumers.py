import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import JsonWebsocketConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .models import FormMessage,Form
import base64
import uuid
from django.conf import settings
import os

consumers = []


class Requests(JsonWebsocketConsumer):
    def connect(self):
        if self.scope["user"].is_anonymous:
            self.close()
            return
        consumers.append(self)
        self.accept()

    def disconnect(self, *args, **kwargs):
        consumers.remove(self)

    def receive_json(self, *args, **kwargs):
        self.send_json({})



class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.room_name = self.scope['url_route']['kwargs']['id']
            self.room_group_name = 'chat_%s' % self.room_name
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive_json(self, content, **kwargs):
        message = content.get('content')
        image_raw = content.get('image')
        username = self.scope["user"]
        if image_raw != None:
            if (image_raw.__contains__("data:application/octet-stream;base64,")):
                image_raw = image_raw.replace("data:application/octet-stream;base64,", '')
                image_bytes = base64.b64decode(image_raw)
                filename = f"{uuid.uuid4().hex}.png"
                file_path = os.path.join(settings.MEDIA_ROOT, filename)
                with open(file_path, 'wb') as file:
                    file.write(image_bytes)
            else:
                format, image_data = image_raw.split(';base64,')
                ext = format.split('/')[-1]
                filename = f"{uuid.uuid4().hex}.{ext}"
                file_path = os.path.join(settings.MEDIA_ROOT, filename)
                decoded_image = base64.b64decode(image_data)
                with open(file_path, 'wb') as file:
                    file.write(decoded_image)      
        else:
            filename = ''    
        form = await sync_to_async(Form.objects.get)(pk=self.scope['url_route']['kwargs']['id'])
        form_message = await sync_to_async(FormMessage.objects.create)(
            message=message,
            image=filename,
            user=username
        )
        await sync_to_async(form.messages.add)(form_message)
        image_url = form_message.image_thumbnail.url if form_message.image_thumbnail else ''
        image_url_src = form_message.image.url if form_message.image else ''
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'content': message,
                'image': image_url,
                'image_src': image_url_src,
                'username': (f'{username.first_name} {username.last_name}'),
            }
        )

    async def chat_message(self, event):
        content = event.get('content')
        image = event.get('image')
        image_url_src = event.get('image_src')
        username = event.get('username')
        await self.send_json({
            'type_event': 'new_chat_message',
            'content': content,
            'image': image,
            'image_src': image_url_src,
            'username': username,
        })