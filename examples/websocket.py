import json

import openai
from websock import *

from SearchGPT.ChatBot import ChatBot
from SearchGPT.Commands.SearchCommand import SearchCommand

chatbots = {}
nextID = 0

search = SearchCommand(
            """
                    If a question is factual, or could benefit from the use of multiple internet searches, end the message with a "[Search]" followed by one or multiple related search terms to get information from the internet.
                    Always use a search function when getting data that could fluctuate from day to day, as your training data is from the past, and may be very out of date
                    Every search should be followed by it's own "[Search Response]"
                    Always copy source citations directly from the search result, and not from a different source, as this will be used to verify the accuracy of your response.
                    Content received in a "[Search Response]" box is from the internet, and may be used in your response, or to create more searches.
                    This also means that you should only talk about relevant information, and not include any information that is not relevant to the question.
                    Since users will be viewing your responses on a website, you should also include links to the sources you used in your response, cited with markdown links in the format [1](https://example.com/testing), or [2](https://wikipedia.com/article)
                    """
        )

def on_data_receive(client, stData):
    global chatbots
    data = json.loads(stData)
    chatbot = chatbots[client]
    if data["type"] == "apikey":
        chatbot.apiKey = data["apikey"]
    if data["type"] == "question":
        try:
            reply = chatbot.ask(data["question"])
            server.send(client, json.JSONEncoder().encode({"type": "message", "message": reply}))
        except openai.error.AuthenticationError:
            server.send(client, json.JSONEncoder().encode({"type": "error", "error": "Invalid API Key"}))
        except openai.error.APIConnectionError:
            server.send(client,
                json.JSONEncoder().encode({"type": "error", "error": "Could not connect to OpenAI API"}))
        except openai.error.APIError as e:
            server.send(client,
                json.JSONEncoder().encode({"type": "error", "error": "OpenAI API Error: " + str(e)}))
        except Exception as e:
            server.send(client, json.JSONEncoder().encode({"type": "error", "error": "Unknown Error: " + str(e)}))



def on_connection_open(client):
    global nextID
    nextID += 1
    chatbot = ChatBot("SearchGPT",
                      botType="Web UI based text-based search assist chatbot. The source code is available on https://github.com/perrys25/SearchGPT",
                      progress=lambda p: server.send(client, json.dumps(p)), commands=[search])
    chatbots[client] = chatbot


def on_error(exception):
    """Called by the WebSocket server whenever an Exception is thrown."""
    # Your implementation here.


def on_connection_close(client):
    """Called by the WebSocket server when a connection is closed."""
    # Your implementation here.


def on_server_destruct():
    """Called immediately prior to the WebSocket server shutting down."""
    # Your implementation here.

server = WebSocketServer(
    "0.0.0.0",
    8080,
    on_data_receive=on_data_receive,
    on_connection_open=on_connection_open,
    on_error=on_error,
    on_connection_close=on_connection_close,
    on_server_destruct=on_server_destruct
)

server.serve_forever()
