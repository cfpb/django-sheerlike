from __future__ import absolute_import  # Python 2 only

import functools

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse

from jinja2 import Environment, StrictUndefined

from .query import QueryFinder, more_like_this, get_document
from .filters import selected_filters_for_field, is_filter_selected
from .templates import date_formatter
from .middleware import get_request

PERMALINK_REGISTRY={}

def register_permalink(sheer_type, url_pattern_name):
    PERMALINK_REGISTRY[sheer_type]=url_pattern_name

def url_for(app, filename):
    if app == 'static':
        return staticfiles_storage.url(filename)
    else:
        raise ValueError("url_for doesn't know about %s" % app)

def date_filter(value, format="%Y-%m-%d"):
        return date_formatter(value, format)


def environment(**options):
    queryfinder = QueryFinder()

    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url_for':url_for,
        'url': reverse,
        'queries': queryfinder,
        'more_like_this': more_like_this,
        'get_document': get_document,
        'selected_filters_for_field': selected_filters_for_field,
        'is_filter_selected': is_filter_selected,
    })
    env.filters.update({
        'date':date_filter
    })
    return env
