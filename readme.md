# SearchGPT
Bringing the Internet, and Chat AI one step closer

## What is SearchGPT?
SearchGPT is a library for using [OpenAI](https://openai.com/)'s GPT-3 Language Model & Google Search to power a Question-Answering Chatbot similar to that of Bing's assistant that can do external research as needed to help answer questions

## How can I try it?
Clone `SearchGPT`'s git Repo
Using Python `3.9`
Run `pip install -r requirements`
Open `examples`
Run `py cli.py`

## How does the API Work?

### ChatBot

The main API is a `ChatBot` class of which you can create an instance, and ask questions
An example of creating a bot named "Steve" who thought he was voice activated would be the following:
```py
bot = ChatBot("Steven", type="Voice activated search assist chatbot", commands=[SearchCommand()])
bot.ask("What's the weather like right now?")
```

### Commands

Commands help the bot perform actions. two example command are the `SearchCommand` used for searching google, or the FollowUP command inside the `cli.py` UI used for asking secondary questions when needed

An example for a fictional home assistant controller would be:
```py
class LightsCommand(Command):
    def getName(cls):
        return "Lights"

    def getDescription(cls):
        return """
           If the user has asked to turn out the lights in a specific room (which must be decided on beforehand, possibly with a followup), use the "[Lights] Off RoomName" Command
           It will always be followed by a "[Lights Response]" command either containing "Success", or an encountered error while disabling lights
           """

    def execute(self, chatbot, data, question):
        if data.split(" ")[0] == "Off":
            # Turn off lights
            return "Success"
        return "Failure, invalid command"
```