smart-urlize
============

smart-urlize is licensed under [MIT license](LICENSE.md).

The purpose of this django app is to provide an easy way to detect and handle urls in texts.
Different urls are handled in different ways. For instance, an image url is wrapped in a html img tag and a youtube url is replaced by an embedded youtube player.
Urls that are not known how to handle and email addresses are replaced by actual html links.

# Usage
First, add `smarturlize` to your installed apps.

The easies way to use this app is to simply add the template filter `smart_urlize` to a text in your template.
```django
{% load smart_urlize %}

{{ text|smart_urlize }}

```
Just be aware that the `smart_urlize` template filter marks the text as safe.
It is therefore important to make sure that your text is
[escaped](https://docs.djangoproject.com/en/dev/ref/templates/builtins/#std:templatefilter-escape)
if it comes from user input to prevent XSS attacks.

# Write your own url handlers
Adding your own url transformers is very easy.  
You do that by writing a custom transformer class which should be a subclass of
[`transformers.BaseTransformer`](smarturlize/transformers.py#L5-L28).  
You can then register your transformer with the `@transformer` decorator.

```python
from smarturlize.transformers import BaseTransformer, transformer


@transformer
class MakeRedditLinksGreen(BaseTransformer):

    def match(self, word):
        return word.url.hostname in ('reddit.com', 'www.reddit.com')

    def transform(self, word):
        return '<a style="color: green;" href="%s">Reddit link</a>' % word.word
```

```python
>>> from smarturlize import SmartUrlize
>>> urlizer = SmartUrlize()
>>> print urlizer('This contains a reddit link http://www.reddit.com/r/programming')
This contains a reddit link <a style="color: green;" href="http://www.reddit.com/r/programming">Reddit link</a>
```

### Handling non urls

By default, smart-urlize will check each word if it is an url before trying to transform it.
This is done for performance reasons so the non urls in your text, won't be parsed through all of the transfomers.

However, you can also create a transformer that works on non urls if you want to.
This is done by adding the `is_url_handler = False` property to your transformer class.
Let's say you wan't to correct all misspellings of the word 'belive' to 'believe'.
In that case your transformer class would look something like this.

```python
from smarturlize.transformers import BaseTransformer, transformer


@transformer
class CorrectTypoBelive(BaseTransformer):

    is_url_handler = False
    
    def match(self, word):
        return word.word == 'belive'
        
    def transform(self, word):
        return 'believe'
```

### Unregistering url handlers

To unregister an url handler, call `smarturlize.registry.unregister` with the transformer's class name as an argument.
```python
from smarturlize import registry

registry.unregister('DisplayImages')
```
