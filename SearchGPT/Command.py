import abc

class Command(abc.ABC):
    @abc.abstractclassmethod
    def getName(cls) -> str:
        pass

    @abc.abstractclassmethod
    def getDescription(cls) -> str:
        pass

    @abc.abstractclassmethod
    def execute(cls, chatbot, input: str, question: str) -> str:
        pass