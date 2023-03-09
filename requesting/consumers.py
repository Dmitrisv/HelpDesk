from channels.generic.websocket import JsonWebsocketConsumer

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
