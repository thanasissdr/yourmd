from typing import List
import unittest
from unittest.mock import MagicMock, patch

import numpy as np
from parameterized import parameterized

from flaskr.preprocess import (
    LowerCase,
    PreprocessorTokenwise,
    RemoveShort,
    SpaceRemover,
    RemoveStopwords,
)


def mock_token_strategy_run_result(sentence: str) -> List:
    """
    Mock token strategy run result which will
    result in either the token itself or
    a None value
    """
    np.random.seed(42)
    res = []
    for token in sentence.split():
        res.append(np.random.choice([None, token], p=[0.5, 0.5]))
    return res


class TestPreprocess(unittest.TestCase):
    @parameterized.expand([("ABC", "abc"), ("A!C", "a!c")])
    def test_lowercase(self, input: str, output: str):
        lower = LowerCase().run(input)
        self.assertEqual(lower, output)

    @parameterized.expand(
        [("", 1, None), ("a", 1, "a"), ("ab", 2, "ab"), ("ab", 3, None)]
    )
    def test_remove_short(self, input: str, min_token_length: int, output: str):
        self.assertEqual(
            RemoveShort(min_token_length=min_token_length).run(input), output
        )

    @parameterized.expand(
        [("a", "a"), (" ab", "ab"), ("  ab", "ab"), ("ab ", "ab"), ("abc  ", "abc")]
    )
    def test_remove_space(self, input, output):
        self.assertEqual(SpaceRemover().run(input), output)

    @parameterized.expand(
        [("ab", None, "ab"), ("ab", ["ab"], "ab"), ("abc", ["ab"], None)]
    )
    def test_extract_tokens(self, input, terms, output):
        self.assertEqual(RemoveStopwords(stopwords=terms).run(input), output)

    @parameterized.expand([("This is a simple sentence", 5), ("one", 1), ("", 0)])
    def test_preprocessor_tokenwise_calls(
        self, sentence: str, expected_number_of_token_strategy_run_calls: int
    ):

        mock_token_strategy = MagicMock()
        mock_token_strategy.run = MagicMock(
            side_effect=mock_token_strategy_run_result(sentence)
        )

        preprocessor_tokenwise = PreprocessorTokenwise(
            token_strategy=mock_token_strategy
        )
        preprocessor_tokenwise.run(sentence)

        self.assertEqual(
            preprocessor_tokenwise.token_strategy.run.call_count,
            expected_number_of_token_strategy_run_calls,
        )
