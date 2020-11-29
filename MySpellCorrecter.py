from tokenize import tokenize

from nltk import word_tokenize
from rasa.nlu.components import Component
from rasa.nlu import utils
from rasa.nlu.model import Metadata

import nltk
import re
from spellchecker import SpellChecker
import os


def untokenize(words):
    """
    Tokenizált szavakat/írásjeleket visszaállít az eredeti állapotába. Ha egy szövegre meghívjuk a tokenize() függvényt,
    akkor ez a függvény visszaállítja a tokenizálás előtti állapotát a szövegnek.
    """
    text = ' '.join(words)
    step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .', '...')
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
    step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
    step5 = step4.replace(" '", "'").replace(" n't", "n't").replace(
        "can not", "cannot")
    step6 = step5.replace(" ` ", " '")
    return step6.strip()


class MySpellCorrecter(Component):

    name = "spellcorrecter"
    provides = ["message"]
    requires = ["message"]
    defaults = {}
    language_list = ["en"]

    def __init__(self, component_config=None):
        super(MySpellCorrecter, self).__init__(component_config)

    def train(self, training_data, cfg, **kwargs):
        pass

    def process(self, message, **kwargs):
        """Retrieve the text message, pass it to the classifier
            and append the prediction results to the message class."""

        spc = SpellChecker()
        res = word_tokenize(message.text)
        [print("before -> ", word) for word in res]

        new_words = []
        for word in res:
            new_words.append(spc.correction(word))
        [print("after -> ", spc.correction(word)) for word in res]

        message.text = untokenize(new_words)
        message.set("text", message.text, True)
        print("The corrected sentence -> ", untokenize(new_words))

    def persist(self, file_name, model_dir):

        pass

    @classmethod
    def required_packages(self):
        return []
