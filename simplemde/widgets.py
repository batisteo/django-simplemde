from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse_lazy
from django.conf import settings

from .utils import json_dumps


GLOBAL_OPTIONS = getattr(settings, 'SIMPLEMDE_OPTIONS', {})


class SimpleMDEEditor(widgets.Textarea):
    def __init__(self, *args, **kwargs):
        self.custom_options = kwargs.pop('simplemde_options', {})
        super(SimpleMDEEditor, self).__init__(*args, **kwargs)

    @property
    def options(self):
        options = GLOBAL_OPTIONS.copy()
        options.update(self.custom_options)
        return options

    def render(self, name, value, attrs=None):
        if 'class' not in attrs.keys():
            attrs['class'] = ''

        attrs['class'] += ' simplemde-box'

        attrs['data-simplemde-options'] = json_dumps(self.options)

        html = super(SimpleMDEEditor, self).render(name, value, attrs)

        return mark_safe(html)

    def _media(self):
        js = (
            'simplemde/simplemde.min.js',
            'simplemde/simplemde.init.js'
        )

        css = {
            'all': (
                'simplemde/simplemde.min.css',
            )
        }
        return forms.Media(css=css, js=js)
    media = property(_media)