from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse
import json

ws = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off" placeholder="city:period:hour"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@ws.get("/")
async def get():
    return HTMLResponse(html)

data_path = './WeatherPredictorApi/data'
cities = open(f'{data_path}/cities.json')
citiesData = json.load(cities)

periods=['hourly','daily', 'weekly']

@ws.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        data = data.split(":")
        if len(data)!=3:
            await websocket.send_text('wrong format')
        else:
            if data[0] not in citiesData:
                await websocket.send_text('City not supported')
            elif data[1] not in periods:
                await websocket.send_text(f'Period not suppored, supported periods are {periods}')
            else: 
                await websocket.send_text(f"Message text was: {data}")