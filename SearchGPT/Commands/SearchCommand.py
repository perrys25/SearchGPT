from SearchGPT.Command import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import urllib.parse


class SearchCommand(Command):

    def __init__(self, description="""
        If a question is factual, or could benefit from the use of multiple internet searches, end the message with a "[Search]" followed by one or multiple related search terms to get information from the internet.
        Always use a search function when getting data that could fluctuate from day to day, as your training data is from the past, and may be very out of date
        Search should only contain 1-10 search terms written in a way that would be used in a google search, and should be separated by spaces, not meant to be readable by humans
        """,
                 question="""
            In the below content, links are shown below the title for a result, and above the actual information. You should always use Markdown Link Formatting should be used to cite where specific information came from, and to provide a link to the source, in the style of [Content](Link) Example: The verb "define" means used to refer to somebody/something that has already been mentioned or is easily understood[1](https://www.oxfordlearnersdictionaries.com/us/definition/english/define)
            All citing should be done inline not at the end of the entire response, to links that were previously referenced in the search result, and should be from the most reputable sources their (Encyclopedias, News Outlets, etc)
            Try to cite at least two sources for any claim, using inline citation notation of 1, 2, 3, etc
            Every single link must be copied from the search result, and not from a different source, as this will be used to verify the accuracy of your response.
            Please respond with a sentence or two markdown-styled answer summarizing only useful & very topical points (specific to the question: {question}) about the above search result, making sure to always cite sources using the aforementioned inline source citing technique.                 
            
            Again, most importantly, always use links found in user input, and never use links you have no seen before."""):
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
        self.driver.get('http://www.google.com/search?q=' + urllib.parse.quote_plus(input))
        chatbot.progress({"type": "Search", "search": input})
        self.driver.execute_script(
            "[...document.getElementsByTagName('cite')].map(cite => { cite.innerHTML = cite.parentElement.parentElement.parentElement.parentElement.href; return cite.parentElement.parentElement.parentElement.parentElement.href})")
        answer = self.driver.execute_script(
            "return [...document.querySelectorAll(arguments[0])].filter(a => a.textContent === arguments[1])[0].parentElement.parentElement.innerText.substring(arguments[2], arguments[3])",
            "h1", "Search Results", 0, 5000)
        summary = chatbot.completion([
            {"role": "system", "content": self.question.replace("{question}", question)},
            {"role": "user", "content": answer},
            {"role": "user", "content": self.question.replace("{question}", question)},
        ], 512, 0.2).content.strip()
        chatbot.progress({"type": "Search Response", "response": summary})
        return summary
