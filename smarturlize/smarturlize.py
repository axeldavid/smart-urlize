import re
import urlparse

from .transformers import (ClickableLinks, DisplayImages, EmailLinks,
                           YoutubeEmbed)


class Word(object):

    def __init__(self, word):
        self.word = word
        self.get_url()

    def get_url(self):
        self.is_url = bool(re.match(
            'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F]'
            '[0-9a-fA-F]))+', self.word
        ))
        self.url = self.is_url and urlparse.urlparse(self.word) or None


class SmartUrlize(object):

    def get_transformers(self):
        return [t() for t in self.Meta.transformers]

    def transform_word(self, word):
        for t in self.transformers:
            if (word.is_url or not t.is_url_handler) and t.match(word):
                return t.transform(word)
        return word.word

    def transform(self):
        self.words = [Word(w) for w in self.text.split(' ')]
        self.transformers = self.get_transformers()
        for i, w in enumerate(self.words):
            self.words[i] = self.transform_word(w)

    def __call__(self, text):
        self.text = text
        self.transform()
        return ' '.join(self.words)

    class Meta:
        '''All transfomers that will be used for the text.

        New transformers can be added here. Note that only the first
        transformer that matches the word will be used. So make sure that if
        you want your transformer to have a higher priority than e.g.
        ClickableLinks, it has to be placed before the ClickableLinks
        transformer in the list.
        '''
        transformers = [DisplayImages, YoutubeEmbed, EmailLinks,
                        ClickableLinks]
