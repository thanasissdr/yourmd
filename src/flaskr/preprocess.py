from abc import ABC, abstractmethod
from functools import reduce
from typing import Callable, List, Optional


class TokenStrategy(ABC):
    @abstractmethod
    def run(self, token: str):
        pass


class RemoveShort(TokenStrategy):
    def __init__(self, min_token_length: int = 1):
        self.min_token_length = min_token_length

    def run(self, token: str):
        if self.is_short(token):
            return None
        return token

    def is_short(self, token: str) -> bool:
        if len(token) < self.min_token_length:
            return True
        return False


class RemoveStopwords(TokenStrategy):
    def __init__(self, stopwords: Optional[List[str]] = None):
        self.stopwords = stopwords

    def run(self, token):
        if self.stopwords:
            return token if token not in self.stopwords else None

        return token


class SentencePreprocessor(ABC):
    @abstractmethod
    def run(self, sentence: str):
        pass


class PreprocessorTokenwise(SentencePreprocessor):
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


class RemoveExtraSpace(SentencePreprocessor):
    def run(self, sentence: str) -> str:
        return " ".join(sentence.split())


class LowerCase(SentencePreprocessor):
    def run(self, sentence: str) -> str:
        return sentence.lower()


def compose(*functions: Callable):
    return reduce(lambda f, g: lambda x: g(f(x)), functions)


class Preprocessor:
    def __init__(self, preprocessing_steps: List[SentencePreprocessor]):
        self.preprocessing_steps = preprocessing_steps

    def run(self, data: str):
        for preprocessing_step in self.preprocessing_steps:
            data = preprocessing_step.run(data)

        return data
