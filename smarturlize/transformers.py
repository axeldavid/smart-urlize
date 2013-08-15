import re
import urlparse


class BaseTransformer(object):

    is_url_handler = True

    def match(self, word):
        ''' Word matcher

        Args:
            word (smarturlize.smarturlize.Word)
        Returns:
            (bool): Indicates wheather the given word object should be handled
            by this transformer or not.
        '''
        raise NotImplementedError

    def transform(self, word):
        ''' Word transformer

        Args:
            word (smarturlize.smarturlize.Word)
        Returns:
            (str) The string you want to replace the given word with.
        '''
        raise NotImplementedError


class ClickableLinks(BaseTransformer):
    '''Converts urls to clickable links'''

    def match(self, word):
        return True

    def transform(self, word):
        return '<a href="%s">%s</a>' % (word.word, word.url.query)


class DisplayImages(BaseTransformer):
    '''Wraps urls in html img tags'''

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
