from rasa.nlu.components import Component
from rasa.nlu import utils
from rasa.nlu.model import Metadata

import nltk
from spellchecker import SpellChecker
import os


class SpellCorrecter(Component):
    """A pre-trained sentiment component"""

    name = "sentiment"
    provides = ["entities"]
    requires = []
    defaults = {}
    language_list = ["en"]

    def __init__(self, component_config=None):
        super(SpellCorrecter, self).__init__(component_config)

    def train(self, training_data, cfg, **kwargs):
        """Not needed, because the the model is pretrained"""
        pass

    def process(self, message, **kwargs):
        """Retrieve the text message, pass it to the classifier
            and append the prediction results to the message class."""

        spc = SpellChecker()
        res = spc.split_words(message.text)
        [spc.correction(word) for word in res]

        message_result = [word + " " for word in res]
        message.text = message_result

    def persist(self, model_dir):
        """Pass because a pre-trained model is already persisted"""

        pass
