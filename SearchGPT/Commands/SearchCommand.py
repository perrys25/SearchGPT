from SearchGPT.Command import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import urllib.parse


class SearchCommand(Command):

    def __init__(self):
        options = Options()
        options.add_argument("--window-size=1024x768")
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
    def getName(cls):
        return "Search"

    def getDescription(cls):
        return """
        If a question is factual, or could benifit from the use of multiple internet searches, end the message with a "[Search]" followed by one or multiple related search terms to get information from the internet.
        Always use a search function when getting data that could fluctuate from day to day, as your training data is from the past, and may be very out of date
        Every search should be followed by it's own "[Search Response]"
        Content received in a "[Search Response]" box is from the internet, and may be used in your response, or to create more searches.
        """

    def execute(self, chatbot, input, question):
        self.driver.get('http://www.google.com/search?q=' + urllib.parse.quote_plus(input))
        chatbot.progress({"type": "Search", "search": input})
        answer = self.driver.execute_script(
            "return [...document.querySelectorAll(arguments[0])].filter(a => a.textContent === arguments[1])[0].parentElement.innerText.substring(arguments[2], arguments[3])",
            "h1", "Search Results", 0, 2500)
        summary = chatbot.completion(
            answer + "\n\n\nMulti-sentance (possible multi-paragraph) answer sumarizing key points (specific to the question: " + question + " about the above search result: ",
            1024).strip()
        chatbot.progress({"type": "Search Response", "response": summary})
        return summary
