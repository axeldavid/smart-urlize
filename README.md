smart-urlize
============

smart-urlize is licensed under MIT license.

The purpose of this django app is to provide an easy way to detect and handle urls in texts.
Different urls are handled in different ways. For instance, an image url is wrapped in a html img tag and a youtube url is replaced by an embedded youtube player.
Urls that are not known how to handle and email addresses are replaced by actual html links.

# Usage
The easies way to use this app is to simply add the template filter `smart_urlize` to a text in your template.
Just remember to also use the `safe` filter on the text since `smart_urlize` will add html tags to it.
```django
{% load smart_urlize %}

{{ text|smart_urlize|safe }}

```
And of course, always make sure that all content that comes from user input is [escaped](https://docs.djangoproject.com/en/dev/ref/templates/builtins/#std:templatefilter-escape) before displaying it on your website.

# Write your own url handlers
Adding your own url transformers is very easy.
You can create a custom transformer class which should be a subclass of `transformers.BaseTransformer` where you override two methods, `match` and `transform`.
These methods take a parameter `word` which is not a string but an instance of the class `smarturlize.Word`.
The `match` method should return a boolean value, whether the word should be handled by this transformer or not.
The `transform` method should return a string that represents the transformed value.
Finally, add the new transformer to `smarturlize.SmartUrlize.Meta.transformers`.

```python
from smarturlize.transformers import BaseTransformer
from smarturlize import SmartUrlize

class MakeRedditLinksGreen(BaseTransformer):

    def match(self, word):
        return word.url.netloc.endswith('reddit.com')

    def transform(self, word):
        return '<a style="color: green;" href="%s">%s</a>' % (word.word, word.url.query)


text = 'This is a text containing a reddit link http://www.reddit.com/r/programming'
urlizer = SmartUrlize()
urlizer.Meta.transformers.insert(0, MakeRedditLinksGreen)
print urlizer(text)
```
