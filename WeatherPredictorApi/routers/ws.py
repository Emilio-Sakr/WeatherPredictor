from fastapi import APIRouter, WebSocket
from WeatherPredictorApi.routers.cities import findCitiesJson

ws = APIRouter()

periodIntervals = ['hourly','every_5_hours', 'every_10_hours', 'daily', 'every_2_days', 'every_3_days', 'weekly']

@ws.websocket_route('/')
async def wsRoute(websocket: WebSocket, city: str):
    await websocket.accept()
    await websocket.send_text('Websockets Route')
    await websocket.close()