import abc


class Command(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def getName(cls) -> str:
        pass

    @classmethod
    @abc.abstractmethod
    def getDescription(cls) -> str:
        pass

    @classmethod
    @abc.abstractmethod
    def execute(cls, chatbot, input: str, question: str) -> str:
        pass
