from typing import List

from flask import jsonify, request

from flaskr import app, db
from flaskr.models import MedicalTerms
from flaskr.preprocess import (
    LowerCase,
    PreprocessorTokenwise,
    RemoveShort,
    RemoveStopwords,
    RemoveExtraSpace,
    Preprocessor,
)

from profilers import timing

preprocessor = Preprocessor(
    [
        LowerCase(),
        PreprocessorTokenwise(
            RemoveStopwords(stopwords=["a", "an", "and", "at", "in", "on", "of", "the"])
        ),
        PreprocessorTokenwise(RemoveShort(min_token_length=3)),
        RemoveExtraSpace(),
    ]
)


@app.route("/", methods=["GET"])
def getter():
    args = request.args
    sentence = args["text"]
    preprocessed_text = preprocessor.run(sentence)

    all_results = [res.medical_term for res in db.session.query(MedicalTerms).all()]

    res = search(preprocessed_text, all_results)

    if len(res) >= 1:
        return jsonify(res)

    else:
        return jsonify("No terms found in the dataset")


@timing
def search(sentence: str, phrases_list: List[str]) -> List[str]:
    """
    Args:
        phrases_list: List of terms
    Returns:
        Results found in phrases_list which contain terms in the input sentence
    """

    res = []
    for phrase in phrases_list:
        if any(term in phrase.split() for term in sentence.split()):
            res.append(phrase)
    return res
