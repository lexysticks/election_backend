# vote/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class VoteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # URL route: /ws/votes/<election_type>/
        self.election_type = self.scope["url_route"]["kwargs"]["election_type"]
        self.group_name = f"election_{self.election_type}"

        # join group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # leave group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Receive message from group
    async def party_counts_update(self, event):
        # event contains {"type": "party_counts_update", "payload": {...}}
        payload = event.get("payload", {})
        # send to WebSocket
        await self.send(text_data=json.dumps({"type": "party_counts_update", "payload": payload}))
