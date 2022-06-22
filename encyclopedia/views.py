from django.shortcuts import redirect, render
from django.urls import reverse
from markdown2 import Markdown

from . import util
from . import forms

def render_helper(request, link, context={}):
    if context.get('search') == None:
        context['search'] = forms.SearchForm()

    context['entries'] = util.list_entries()
    
    return render(request, link, context)

def index(request):
    return render_helper(request, "encyclopedia/index.html")

def error(request, title):
    return render_helper(request, "encyclopedia/error.html", {'title': title})

def entry(request, title):
    entry = util.get_entry(title)

    if entry != None:
        markdowner = Markdown()

        return render_helper(request, "encyclopedia/entry.html", {
            'title': title,
            'entry': markdowner.convert(entry)
        })

    return error(request, title)

def create(request):
    if request.method == 'POST':
        form = forms.NewEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['entry']
            util.save_entry(title, content)

            return redirect(reverse('entry', args=[title]))
    else:
        form = forms.NewEntryForm()

    return render_helper(request, "encyclopedia/create.html", {'form': form})

def edit(request, title):
    if request.method == 'POST':
        form = forms.EditEntryForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']
            util.save_entry(title, content)

            return redirect(reverse('entry', args=[title]))

    content = util.get_entry(title)
    if content == None: error(request, title)

    return render_helper(request, "encyclopedia/edit.html", {
        'title': title,
        'form': forms.EditEntryForm(initial={'content': content})
    })

def random(request):
    title = util.random_entry()
    return redirect(reverse('entry', args=[title]))

def search(request):
    context = {
        'title': None,
        'search': None,
        'matches': None
    }

    if request.method == 'POST':
        form = forms.SearchForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            context.update({'title': title})
            context.update({'search': forms.SearchForm(initial={'title': title})})

            if util.get_entry(title) != None:
                return redirect(reverse('entry', args=[title]))
            
            matches = util.matching_entries(title)
            context.update({'matches': matches})
    
    return render_helper(request, "encyclopedia/search.html", context)