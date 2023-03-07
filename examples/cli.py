from SearchGPT.ChatBot import *
from SearchGPT.Command import *
from SearchGPT.Commands.SearchCommand import *

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
WHITE = "\033[0;37m"


class FollowupCommand(Command):
    def getName(cls):
        return "Followup"

    def getDescription(cls):
        return """
           If a question could use more objective information, or you have a specific question for the user that could help answer the question, use the "[Followup]" command
           Every followup should be followed by it's own "[Followup Response]"
           Content received in a "[Followup Response]" is from the user directly, and should be taken into consideration along with the "[User]" box as clarification
           """

    def execute(self, chatbot, data, question):
        followup = input(WHITE + "FOLLOWUP QUESTION: " + data + "\n" + GREEN + "INPUT: ")
        return followup


def printProgress(report):
    if report["type"] == "Search":
        print(YELLOW + "PROGRESS: " + "Searching for " + report["search"])
    elif report["type"] == "Search Response":
        print(YELLOW + "PROGRESS: " + report["response"])


chatbot = ChatBot("Victoria", botType="text-based search assist chatbot",
                  purpose="answer people's questions in the most factual way possible, while keeping the length down as long as it is possible without removing content",
                  progress=printProgress, commands=[SearchCommand(), FollowupCommand()])

if chatbot.apiKey is None:
    chatbot.apiKey = input(WHITE + "QUESTION: What is your OpenAI API Key?\n" + GREEN + "INPUT: ")

while True:
    question = input(WHITE + "QUESTION: " + "How can I help?\n" + GREEN + "INPUT: ")
    answer = chatbot.ask(question)
    print(GREEN + "ANSWER: " + answer)
