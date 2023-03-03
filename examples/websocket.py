import asyncio
import json

import openai
import websockets

from SearchGPT.ChatBot import ChatBot


async def handler(websocket, path):
    chatbot = ChatBot("SearchGPT", type="Web UI based text-based search assist chatbot")
    while True:
        data = json.JSONDecoder().decode(await websocket.recv())
        if data["type"] == "apikey":
            chatbot.apiKey = data["apikey"]
        if data["type"] == "question":
            reply = chatbot.ask(data["question"])
            try:
                await websocket.send(json.JSONEncoder().encode({"type": "message", "message": reply}))
            except openai.error.AuthenticationError:
                await websocket.send(json.JSONEncoder().encode({"type": "error", "error": "AuthenticationError"}))


start_server = websockets.serve(handler, "localhost", 8080)

asyncio.get_event_loop().run_until_complete(start_server)

asyncio.get_event_loop().run_forever()
