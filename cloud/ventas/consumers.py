# @Author: Manuel Rodriguez <valle>
# @Date:   11-Mar-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 13-Mar-2018
# @License: Apache license vesion 2.0


from channels.generic.websocket import WebsocketConsumer
import json

class VentasConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.send(text_data=json.dumps({
            'message': message
        }))
