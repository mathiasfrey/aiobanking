import asyncio
import json
import typing
from mysql.connector import (connection)

# https://github.com/iwpnd/geo-stream-kafka/blob/master/geostream/consumer/app/main.py

from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI
from fastapi import WebSocket
from starlette.endpoints import WebSocketEndpoint
from starlette.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel
from pydantic import StrictStr

app = FastAPI(title='aiobanking frontend')
app.add_middleware(CORSMiddleware, allow_origins=["*"])

class ConsumerResponseProcessed(BaseModel):
    account: StrictStr
    balance: int
    modeloutput: float

async def consume(consumer, topicname):
    async for msg in consumer:
        return msg.value.decode()


@app.websocket_route("/ws")
class WebsocketConsumer(WebSocketEndpoint):
    """
    Consume messages from <topicname>
    This will start a Kafka Consumer from a topic
    And this path operation will:
    * return ConsumerResponse
    """

    async def on_connect(self, websocket: WebSocket) -> None:
        topicname = 'account_processed'

        await websocket.accept()
        await websocket.send_json({"Message: ": "connected"})

        loop = asyncio.get_event_loop()
        self.consumer = AIOKafkaConsumer(
            topicname,
            loop=loop,
            client_id='aiobanking-soa',
            bootstrap_servers="kafka:9092",
            enable_auto_commit=False,
        )

        await self.consumer.start()

        self.consumer_task = asyncio.create_task(
            self.send_consumer_message(websocket=websocket, topicname=topicname)
        )

        logger.info("connected")

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        self.consumer_task.cancel()
        await self.consumer.stop()
        logger.info(f"counter: {self.counter}")
        logger.info("disconnected")
        logger.info("consumer stopped")

    async def on_receive(self, websocket: WebSocket, data: typing.Any) -> None:
        await websocket.send_json({"Message: ": data})

    async def send_consumer_message(self, websocket: WebSocket, topicname: str) -> None:
        self.counter = 0
        while True:
            data = await consume(self.consumer, topicname)
            response = ConsumerResponseProcessed(topic=topicname, **json.loads(data))
            logger.info(response)
            await websocket.send_text(f"{response.json()}")
            self.counter = self.counter + 1

@app.websocket_route("/ws-raw")
class WebsocketConsumer(WebSocketEndpoint):
    """
    R/T stream from CDC
    """

    async def on_connect(self, websocket: WebSocket) -> None:
        topicname = 'current_currentaccount'

        await websocket.accept()
        await websocket.send_json({"Message: ": "connected"})

        loop = asyncio.get_event_loop()
        self.consumer = AIOKafkaConsumer(
            topicname,
            loop=loop,
            client_id='aiobanking-soa',
            bootstrap_servers="kafka:9092",
            enable_auto_commit=False,
        )

        await self.consumer.start()

        self.consumer_task = asyncio.create_task(
            self.send_consumer_message(websocket=websocket, topicname=topicname)
        )

        logger.info("connected")

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        self.consumer_task.cancel()
        await self.consumer.stop()
        logger.info(f"counter: {self.counter}")
        logger.info("disconnected")
        logger.info("consumer stopped")

    async def on_receive(self, websocket: WebSocket, data: typing.Any) -> None:
        await websocket.send_json({"Message: ": data})

    async def send_consumer_message(self, websocket: WebSocket, topicname: str) -> None:
        self.counter = 0
        while True:
            data = await consume(self.consumer, topicname)
            #response = ConsumerResponseRaw(topic=topicname, **json.loads(data))
            #logger.info(response)
            #await websocket.send_text(f"{response.json()}")
            await websocket.send_text(data)
            self.counter = self.counter + 1
            
@app.get("/table")
def table():

    cnx = connection.MySQLConnection(
        user='mysqluser', password='mysqlpw',
        host='mysql',
        database='inventory')
    
    cursor = cnx.cursor()

    query = ("SELECT id, account, balance  FROM current_currentaccount")

    cursor.execute(query)
    
    recs = []
    for (id, account, balance) in cursor:
        recs.append(
            {"id": id,
            "account": account,
            "balance": balance}
        )

    cursor.close()

    cnx.close()
    return recs

@app.get("/ping")
def ping():
    return {"ping": "pong!"}