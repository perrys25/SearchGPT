import json

import openai
from SearchGPT.Commands.SearchCommand import *
import re


class ChatBot:
    def __init__(self, name, commands=[SearchCommand()], botType="text-based assist chatbot",
                 purpose="answer people's questions in the most factual way possible, while keeping the length down as long as it is possible without removing content",
                 prompt=
                 """You're a {type} named {name} who's goal is to {purpose} without providing any emotion.
                 As a AI assistant, every message you send starts with one of the following commands surrounded by Square Brackets: ({commands}), and you choose the best one for a given situation""",
                 respond="""The [Response] command is used to respond to a question, and should be used to give factual answers back to the user. The Response command should use plain english, meant for readability""",
                 progress=lambda string: {}, model="gpt-3.5-turbo"):
        # AI Prompt Values
        self.name = name
        self.apiKey = None
        self.commands = commands
        self.commandNames = []
        self.model = model
        for command in commands:
            self.commandNames.append(command.getName())
        self.conversation = [
            {
                "type": "System",
                "value": prompt.replace("{type}", botType).replace("{name}", name).replace("{purpose}", purpose).replace("{commands}", "[" + "], [".join(self.commandNames) + "]")
            },
            {
                "type": "System",
                "value": respond
            }
        ]
        for command in commands:
            self.conversation.append({"type": "System", "value": command.getDescription()})
        self.progress = progress

    def __detokenize(self, values):
        messages = []
        for v in values:
            if v["type"] == "User":
                messages.append({"role": "user", "content": "[User] " + v["value"].strip()})
            elif v["type"] == "Assistant":
                messages.append({"role": "assistant", "content": "[Assistant] " + v["value"].strip()})
            elif self.commandNames.__contains__(v["type"]):
                messages.append({"role": "assistant", "content": "[" + v["type"] + "] " + v["value"].strip()})
            elif v["type"].endswith(" Response"):
                messages.append({"role": "system", "content": "[" + v["type"] + "] " + v["value"].strip()})
            else:
                messages.append({"role": "system", "content": v["value"].strip()})
        return messages

    def __tokenize(self, messages):
        value = []
        for m in messages:
            res = re.search("\[([a-zA-Z]*)] ((.|\n)*)", m["content"])
            if res is not None and m["content"].strip()[0] == "[":
                value.append({"type": res.group(1), "value": res.group(2).strip()})
            else:
                value.append({"type": "Assistant", "value": m["content"].strip()})
        return value

    def completion(self, messages, tokens=512, temperature=0.7):
        data = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            max_tokens=tokens,
            temperature=temperature,
            api_key=self.apiKey
        )
        self.progress({"type": "usedTokens", "value": data["usage"]["total_tokens"]})
        return data.choices[0].message

    def listModels(self):
        models = openai.Model.list(api_key=self.apiKey)["data"]
        output = []
        for model in models:
            name = model["id"]
            # Only chatcompletion models
            if name.startswith("gpt-3.5-turbo") or name.startswith("gpt-4"):
                output.append(name)
        return output

    def ask(self, question):
        self.conversation.append({"type": "User", "value": question})
        i = 0
        while self.conversation[-1]["type"] != "Assistant":
            i += 1
            if i > 4:
                raise Exception("No Response")
            complete = self.conversation[-1]["type"] == "User"
            keep_going = False
            for command in self.commands:
                if self.conversation[-1]["type"] == command.getName():
                    result = command.execute(self, self.conversation[-1]["value"],
                                             question.replace("[", "").replace("]", ""))
                    self.conversation.append({"type": command.getName() + " Response", "value": result})
                    keep_going = True
                    break
                if self.conversation[-1]["type"] == command.getName() + " Response":
                    complete = True
                    break
            if complete:
                response = self.__tokenize(
                    [self.completion(self.__detokenize(self.conversation))])
                self.conversation.extend(response)
            if not complete and not keep_going:
                break
        if self.conversation[-1]["type"] == "Assistant" or self.conversation[-1]["type"] == "Response":
            self.conversation[-1]["type"] = "Assistant"
            return self.conversation[-1]["value"]
        print("DEBUG: " + str(json.dumps(self.conversation)))
        return "Error Returning Answer. Check the console for DEBUG Messages"
