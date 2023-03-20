from SearchGPT.Command import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import urllib.parse


class SearchCommand(Command):

    def __init__(self, description="""Use the "[Search]" command to provide information that requires up-to-date or factual data. The command is a separate response and should be used before any other response commands. Always write search terms as you would in a Google search.
    The search command is the only way to get relevant and factual information, so should be used as often as possible, and should be used to provide information that is not already known to the user. Text written inside a search command should not be human readable, but instead optimized for search engines
    Search commands should be formatted in the following format: "[Search] {search terms}" (without the quotes) where search terms are 1-8 words that are relevant to the question, and act as search terms. No search command should contain any returns
    After a search, never apologize, for your previous response being incorrect.""",
                 question="""In the [Search Result], links are shown above the title for a result, and above the actual information.
            Please respond with between a sentence and paragraph summarizing only useful & very topical points (specific to the question: {question}) about the above search result""",
                 ):
        options = Options()
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.description = description
        self.question = question

    def getName(cls):
        return "Search"

    def getDescription(cls):
        return cls.description

    def execute(self, chatbot, input, question):
        self.driver.get('http://www.google.com/search?q=' + urllib.parse.quote_plus(input.replace("\"", "").split("\n")[0]))
        chatbot.progress({"type": "Search", "search": input.replace("\"", "").split("\n")[0]})
        try:
            self.driver.execute_script(
                "[...document.getElementsByTagName('cite')].map(cite => { cite.innerHTML = cite.parentElement.parentElement.parentElement.parentElement.href; return cite.parentElement.parentElement.parentElement.parentElement.href})")
        except:
            pass
        answer = self.driver.execute_script(
            "return [...document.querySelectorAll(arguments[0])].filter(a => a.textContent === arguments[1])[0].parentElement.parentElement.innerText.substring(arguments[2], arguments[3])",
            "h1", "Search Results", 0, 1500)
        summary = chatbot.completion([
            {"role": "system", "content": self.question.replace("{question}", question)},
            {"role": "user", "content": "[Search Result] " + answer},
            {"role": "user", "content": self.question.replace("{question}", question)},
        ], 512, 0.2).content.strip()
        chatbot.progress({"type": "Search Response", "response": summary})
        return summary
