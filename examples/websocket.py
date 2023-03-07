import asyncio
import json

import openai
import websockets

from SearchGPT.ChatBot import ChatBot
from SearchGPT.Commands.SearchCommand import SearchCommand


async def handler(websocket, path):
    progress = []

    def sendProgress(p):
        progress.append(p)

    chatbot = ChatBot("SearchGPT",
                      botType="Web UI based text-based search assist chatbot. The source code is available on https://github.com/perrys25/SearchGPT",
                      progress=sendProgress, commands=[SearchCommand(
            """
                    If a question is factual, or could benefit from the use of multiple internet searches, end the message with a "[Search]" followed by one or multiple related search terms to get information from the internet.
                    Always use a search function when getting data that could fluctuate from day to day, as your training data is from the past, and may be very out of date
                    Every search should be followed by it's own "[Search Response]"
                    Always copy source citations directly from the search result, and not from a different source, as this will be used to verify the accuracy of your response.
                    Content received in a "[Search Response]" box is from the internet, and may be used in your response, or to create more searches.
                    This also means that you should only talk about relevant information, and not include any information that is not relevant to the question.
                    Since users will be viewing your responses on a website, you should also include links to the sources you used in your response, cited with markdown links in the format [1](https://example.com/testing), or [2](https://wikipedia.com/article)
                    """
        )])
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
                await websocket.send(
                    json.JSONEncoder().encode({"type": "error", "error": "Could not connect to OpenAI API"}))
            except openai.error.APIError as e:
                await websocket.send(
                    json.JSONEncoder().encode({"type": "error", "error": "OpenAI API Error: " + str(e)}))
            except Exception as e:
                await websocket.send(json.JSONEncoder().encode({"type": "error", "error": "Unknown Error: " + str(e)}))


start_server = websockets.serve(handler, "localhost", 8080)

asyncio.get_event_loop().run_until_complete(start_server)

asyncio.get_event_loop().run_forever()
