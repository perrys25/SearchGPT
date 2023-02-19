from SearchGPT.ChatBot import *

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
WHITE = "\033[0;37m"

if openai.api_key == None:
    openai.api_key = input(WHITE + "What is your OpenAI API Key?\n" + GREEN + "INPUT: ")

def printProgress(report):
    if report["type"] == "Search":
        print(YELLOW + "PROGRESS: " + "Searching for " + report["search"])

chatbot = ChatBot("Victoria")
while True:
    question = input(WHITE + "QUESTION: " + "How can I help?\n" + GREEN + "INPUT: ")
    answer = chatbot.ask(question)
    print(GREEN + "ANSWER: " + answer)
