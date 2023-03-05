import asyncio
import json

import openai
import websockets

from SearchGPT.ChatBot import ChatBot


async def handler(websocket, path):
    progress = []
    def sendProgress(p):
        progress.append(p)

    chatbot = ChatBot("SearchGPT", type="Web UI based text-based search assist chatbot. The source code is available on https://github.com/perrys25/SearchGPT", progress=sendProgress)
    while True:
        data = json.JSONDecoder().decode(await websocket.recv())
        if data["type"] == "apikey":
            chatbot.apiKey = data["apikey"]
        if data["type"] == "question":
            try:
                reply = chatbot.ask(data["question"])
                for p in progress:
                    await websocket.send(json.JSONEncoder().encode(p))
                progress.clear()
                await websocket.send(json.JSONEncoder().encode({"type": "message", "message": reply}))
            except openai.error.AuthenticationError:
                await websocket.send(json.JSONEncoder().encode({"type": "error", "error": "Invalid API Key"}))
            except openai.error.APIConnectionError:
                await websocket.send(json.JSONEncoder().encode({"type": "error", "error": "Could not connect to OpenAI API"}))
            except openai.error.APIError as e:
                await websocket.send(json.JSONEncoder().encode({"type": "error", "error": "OpenAI API Error: " + str(e)}))
            except Exception as e:
                await websocket.send(json.JSONEncoder().encode({"type": "error", "error": "Unknown Error: " + str(e)}))



start_server = websockets.serve(handler, "localhost", 8080)

asyncio.get_event_loop().run_until_complete(start_server)

asyncio.get_event_loop().run_forever()
