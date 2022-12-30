from abc import ABC, abstractmethod
from functools import reduce
from typing import Callable, List, Optional


class TokenStrategy(ABC):
    @abstractmethod
    def run(self, token):
        pass


class RemoveShort(TokenStrategy):
    def __init__(self, min_token_length: int = 1):
        self.min_token_length = min_token_length

    def run(self, token: str):
        if self.is_short(token):
            return None
        return token

    def is_short(self, token) -> bool:
        if len(token) < self.min_token_length:
            return True
        return False


class RemoveStopwords(TokenStrategy):
    def __init__(self, stopwords: Optional[List] = None):
        self.stopwords = stopwords

    def run(self, token):
        if self.stopwords:
            return token if token not in self.stopwords else None

        return token


class TextPreprocessor(ABC):
    @abstractmethod
    def run(self, sentence: str):
        pass


class PreprocessorTokenwise(TextPreprocessor):
    def __init__(self, token_strategy: TokenStrategy):
        self.token_strategy = token_strategy

    def run(self, sentence: str) -> str:
        tokenized_sentence = sentence.split()
        res = []
        for token in tokenized_sentence:
            token_to_append = self.token_strategy.run(token)
            if token_to_append:
                res.append(token_to_append)
        return " ".join(res)


class SpaceRemover(TextPreprocessor):
    def run(self, sentence: str) -> str:
        return " ".join(sentence.split())


class LowerCase(TextPreprocessor):
    def run(self, sentence: str) -> str:
        return sentence.lower()


def compose(*functions: Callable):
    return reduce(lambda f, g: lambda x: g(f(x)), functions)
