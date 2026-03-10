import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Notification


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.group_name = f'notifications_{self.user.id}'
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            # Send unread count on connect
            count = await self.get_unread_count()
            await self.send(text_data=json.dumps({
                'type': 'unread_count',
                'count': count,
            }))
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('type') == 'mark_read':
            await self.mark_all_read()
            await self.send(text_data=json.dumps({'type': 'unread_count', 'count': 0}))

    async def notification_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': event['message'],
            'link': event.get('link', ''),
        }))
        count = await self.get_unread_count()
        await self.send(text_data=json.dumps({'type': 'unread_count', 'count': count}))

    @database_sync_to_async
    def get_unread_count(self):
        return Notification.objects.filter(user=self.user, is_read=False).count()

    @database_sync_to_async
    def mark_all_read(self):
        Notification.objects.filter(user=self.user, is_read=False).update(is_read=True)


class ProjectConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.project_id = self.scope['url_route']['kwargs']['project_id']
        self.group_name = f'project_{self.project_id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    async def task_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'task_update',
            'action': event['action'],
            'task_id': event.get('task_id'),
            'data': event.get('data', {}),
        }))
