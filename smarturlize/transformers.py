import re
import urlparse


class BaseTransformer(object):

    is_url_handler = True

    def match(self, word):
        # Returns whether the given word should be transformed by this
        # transformer
        return False  # Boolean

    def transform(self, word):
        # Transformer to replace a word with something else or wrap it for
        # instince in a html tag.
        return word.word  # String


class ClickableLinks(BaseTransformer):
    '''Converts a url to a clickable link '''

    def match(self, word):
        return True

    def transform(self, word):
        return '<a href="%s">%s</a>' % (word.word, word.url.query)


class DisplayImages(BaseTransformer):
    '''Wraps urls to images in a img tag'''

    def match(self, word):
        image_extensions = ['jpg', 'jpeg', 'png', 'gif']
        for ext in image_extensions:
            if word.word.lower().endswith('.%s' % ext):
                return True
        return False

    def transform(self, word):
        return '<img src="%s" />' % word.word


class EmailLinks(BaseTransformer):
    '''Makes email addresses clickable'''

    is_url_handler = False

    def match(self, word):
        return re.match('[\w\.-]+@[\w\.-]+\.\w{2,4}', word.word)

    def transform(self, word):
        return '<a href="mailto:%s">%s</a>' % (word.word, word.word)


class YoutubeEmbed(BaseTransformer):
    '''Converts youtube links to embedded youtube frames'''

    width = '640px'
    height = '390px'

    def match(self, word):
        return word.url.netloc.endswith('youtube.com')

    def transform(self, word):
        youtube_id = urlparse.parse_qs(word.url.query).get('v', '')[0]
        params = {
            'type': 'text/html',
            'src': 'http://www.youtube.com/embed/%s' % youtube_id,
            'height': self.height,
            'width': self.width,
            'frameBorder': '0',
        }
        params_string = ['%s="%s"' % (k, v) for k, v in params.iteritems()]
        return '<iframe %s></iframe>' % ' '.join(params_string)
