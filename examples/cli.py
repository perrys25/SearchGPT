from SearchGPT.ChatBot import *
from SearchGPT.Command import *
from SearchGPT.Commands.SearchCommand import *

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
WHITE = "\033[0;37m"

if openai.api_key == None:
    openai.api_key = input(WHITE + "QUESTION: What is your OpenAI API Key?\n" + GREEN + "INPUT: ")

class FollowupCommand(Command):
    def getName(cls):
        return "Followup"

    def getDescription(cls):
        return """
           If a question could use more information, or you have a specific question for the user that could help answer the question (eg. you would like location for requesting weather), use the "[Followup]" command with a question for the user written in the form of a question with proper punctuation and capitalization
           Every search should be followed by it's own "[Followup Response]"
           Content received in a "[Followup Response]" is from the user directly, and should be taken into consideration along with the "[User]" box as clarification
           """

    def execute(self, chatbot, data, question):
        followup = input(WHITE + "QUESTION: " +  data + "\n" + GREEN + "INPUT: ")
        return followup

def printProgress(report):
    if report["type"] == "Search":
        print(YELLOW + "PROGRESS: " + "Searching for " + report["search"])
    elif report["type"] == "Search Response":
        print(YELLOW + "PROGRESS: " + report["response"])

chatbot = ChatBot("Victoria", type="text-based search assist chatbot", progress=printProgress, commands=[FollowupCommand(), SearchCommand()])
while True:
    question = input(WHITE + "QUESTION: " + "How can I help?\n" + GREEN + "INPUT: ")
    answer = chatbot.ask(question)
    print(GREEN + "ANSWER: " + answer)
