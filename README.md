# django-sheerlike

This is an attempt to port some of our favorite [sheer](https://github.com/cfpb/sheer) features over to Django.

**Current status**: Not usable for any purpose.

**Runs on**: Django 1.8 and Python 2.7

# Philosophy

It's our goal to respect the work that people have put into building sites for Sheer, but also avoid coloring too far outside the lines of how Django works.

# Required changes

The biggest change is that the bundle of files that we were calling a "sheer site", is now best thought of as a set of templates for apps that should be defined in the proper Django form. [cfgov-refresh](https://github.com/cfpb/cfgov-refresh) describes many "apps" (blog, newsroom, activity feed, etc), while [Owning a Home](https://github.com/cfpb/owning-a-home/) probably only describes one.

As stated in [Two Scoops of Django 1.8](http://twoscoopspress.org/products/two-scoops-of-django-1-8):

_"each app should be tightly focused on its task. If an app can’t be explained in a single sentence of moderate length, or you need to say ‘and’ more than once, it probably means the app is too big and should be broken up."_
  
Sheer's URL routing goes away entirely. If a particular URL renders a particular template, it's because it was specified in a Django view. If a template presumes the existence of a "post" item on blog post detail, that object will have to be created in the Django view, and passed into the template context. This is pretty simple, though:

```python
def blog_detail(request, slug):                                                  
  post = get_document(doctype='posts', docid=slug)                             
  return render(request, 'blog/_single.html', context={'post':post) 
```

Almost all of the rest of the sheer machinery is still intact, though: you still have access to the global 'queries' object, and can still call functions like get_document and more_like_this.

## Template tweaks


Eliminate relative template includes/imports. for example, in (cfgov-refresh) blog/index.html:

`{% import "_vars-blog.html" as vars with context %}` 

becomes `{% import "blog/_vars-blog.html" as vars with context %}`

The request object is a context variable now, so in order to reference it in 'imported' templates, [you must specify 'with context'](http://jinja.pocoo.org/docs/dev/templates/#import-context-behavior).

For example, `{% from "macros.html" import share as share %}` becomes `{% from "macros.html" import share as share with context%}`

Also, the [Django request object](https://docs.djangoproject.com/en/1.8/ref/request-response/#httprequest-objects) has different properties and methods than the one available in Flask/sheer.

We'll probably find a few more things, so this list will grow.

## API's and RSS Feeds

We will need to switch to native Django tools for such things.

# Recommendations

- Look for opportunities to replace complicated template logic with python views
- Switch to [Django Pagination](https://docs.djangoproject.com/en/1.8/topics/pagination/)

----

## Open source licensing info
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)
