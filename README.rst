django-sheerlike
================

.. image:: https://travis-ci.org/cfpb/django-sheerlike.svg
    :target: https://travis-ci.org/cfpb/django-sheerlike

This is an attempt to port some of our favorite
`sheer <https://github.com/cfpb/sheer>`__ features over to Django.

**Current status**: sheerlike now lives in the cfgov-refresh repo: https://github.com/cfpb/cfgov-refresh/

There will be no further changes here.

**Runs on**: Django 1.8 and Python 2.7

Philosophy
==========

It's our goal to respect the work that people have put into building
sites for Sheer, but also avoid coloring too far outside the lines of
how Django works.

Required changes
================

The biggest change is that the bundle of files that we were calling a
"sheer site", is now best thought of as a set of templates for apps that
should be defined in the proper Django form.
`cfgov-refresh <https://github.com/cfpb/cfgov-refresh>`__ describes many
"apps" (blog, newsroom, activity feed, etc), while `Owning a
Home <https://github.com/cfpb/owning-a-home/>`__ probably only describes
one.

As stated in `Two Scoops of Django
1.8 <http://twoscoopspress.org/products/two-scoops-of-django-1-8>`__:

*"each app should be tightly focused on its task. If an app can’t be
explained in a single sentence of moderate length, or you need to say
‘and’ more than once, it probably means the app is too big and should be
broken up."*

Sheer's URL routing goes away entirely. If a particular URL renders a
particular template, it's because it was specified in a Django view. If
a template presumes the existence of a "post" item on blog post detail,
that object will have to be created in the Django view, and passed into
the template context. We've provided a generic view that makes this
pretty simple:

.. code:: python

        url(r'^blog/(?P<doc_id>[\w-]+)/$', SheerTemplateView.as_view(
                                        doc_type='posts',
                                        local_name='post',
                                        default_template='blog/_single.html',
                                       ), name='blog_detail'),

Almost all of the rest of the sheer machinery is still intact, though:
you still have access to the global 'queries' object, and can still call
functions like get\_document and more\_like\_this.

Template tweaks
---------------

The `Django request
object <https://docs.djangoproject.com/en/1.8/ref/request-response/#httprequest-objects>`__
has different properties and methods than the one available in
Flask/sheer. We've added some helpers to support existing access patterns, but those should be considered deprecated.

Inline IF statements MUST have an else clause, `otherwise the output is
undefined <http://jinja.pocoo.org/docs/dev/templates/#if-expression>`__

Old:

::

    {% macro format_phone(number) %}
        {%- for char in number -%}
            {{- '(' if loop.index == 1  -}}
            {{ char }}
            {{- ') ' if loop.index == 3  -}}
            {{- '-' if loop.index == 6  -}}
        {%- endfor %}
    {% endmacro %}

New:

::

    {% macro format_phone(number) %}
        {%- for char in number -%}
            {{- '(' if loop.index == 1 else '' -}}
            {{ char }}
            {{- ') ' if loop.index == 3 else '' -}}
            {{- '-' if loop.index == 6 else '' -}}
        {%- endfor %}
    {% endmacro %}
`

API's and RSS Feeds
-------------------

We will need to switch to native Django tools for such things.

See it in action
================

Want to test this out?

These instructions assume you have a local elasticsearch server, already populated by 'sheer index' as documented in the `cfgov-refresh readme <https://github.com/cfpb/cfgov-refresh/blob/flapjack/README.md>`__.

-  Check out `cfgov-django <https://github.com/rosskarchner/cfgov-django>`__ alongside cfgov-refresh. 
-  create a new virtualenv and pip install -r requirements.txt
-  cd into the 'cfgov' directory, and run './manage.py runserver'

You should then be able to see the site running on http://localhost:8000

Run the tests
=============

Install `tox <https://tox.readthedocs.org/en/latest/>`__ and run the 'tox' command from a checkout of this repo.

Recommendations
===============

-  Look for opportunities to replace complicated template logic with
   python views
-  Switch to `Django
   Pagination <https://docs.djangoproject.com/en/1.8/topics/pagination/>`__

--------------

Open source licensing info
--------------------------

1. `TERMS <TERMS.rst>`__
2. `LICENSE <LICENSE.rst>`__
3. `CFPB Source Code
   Policy <https://github.com/cfpb/source-code-policy/>`__

