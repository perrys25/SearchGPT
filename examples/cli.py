from SearchGPT.ChatBot import *
from SearchGPT.Command import *
from SearchGPT.Commands.SearchCommand import *

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
WHITE = "\033[0;37m"

def printProgress(report):
    if report["type"] == "Search":
        print(YELLOW + "PROGRESS: " + "Searching for " + report["search"])
    elif report["type"] == "Search Response":
        print(YELLOW + "PROGRESS: " + report["response"])


chatbot = ChatBot("Victoria", botType="text-based search assist chatbot",
                  progress=printProgress, commands=[SearchCommand()])

if chatbot.apiKey is None:
    chatbot.apiKey = input(WHITE + "QUESTION: What is your OpenAI API Key?\n" + GREEN + "INPUT: ")

while True:
    question = input(WHITE + "QUESTION: " + "How can I help?\n" + GREEN + "INPUT: ")
    answer = chatbot.ask(question)
    print(GREEN + "ANSWER: " + answer)
