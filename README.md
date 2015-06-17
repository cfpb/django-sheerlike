# django-sheerlike

This is an attempt to port some of our favorite [sheer](https://github.com/cfpb/sheer) features over to Django.

**Current status**: Not usable for any purpose.

**Runs on**: Django 1.8 and Python 2.7

# Philosphy

It's our goal to respect the work that people have put into building sites for Sheer, but also avoid coloring too far outside the lines of how Django works.

# What does migration look like?

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

Replace references to 'some_result.permalink' to use [Django's URL reversing system](https://docs.djangoproject.com/en/1.8/ref/urlresolvers/#django.core.urlresolvers.reverse).

this:
```
                 <a class="list_link"
                   href="{{ pop_post.permalink }}">
```

becomes:
```
                 <a class="list_link"
                   href="{{ url('blog_detail', kwargs={'slug':pop_post._id})  }}">
```

Eliminate relative template includes/imports. for example, in (cfgov-refresh) blog/index.html:

`{% import "_vars-blog.html" as vars with context %}` 

becomes `{% import "blog/_vars-blog.html" as vars with context %}`

If you are referencing any context variables (like the 'request' object) in 'imported' templates, be sure to specify 'with context'

For example, `{% from "macros.html" import share as share %}` becomes `{% from "macros.html" import share as share with context%}`


We'll probably find a few more things, so this list will grow.

## API's and RSS Feeds

We will need to switch to native Django tools for such things.

----

## Open source licensing info
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)
