from . import util
from django.views import generic
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse 
from django import forms
from random import randint


class NewForm(forms.Form):
    title = forms.CharField(label="Title")
    text = forms.CharField(label="Text")

class NewFormEdit(forms.Form):
    text = forms.CharField(label="Text")


class SearchResultsView(ListView):
    model = util.list_entries()
    template_name = 'search_results.html'
    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = model.objects.filter(
            Q(name__icontains=query) | Q(state__icontains=query)
        )
        return object_list


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    q = request.GET.get('q').strip()
    if q.capitalize() in util.list_entries():
        return redirect("page", title=q)
    return render(request, "encyclopedia/search_results.html", {"entries": util.search(q), "q": q})

    # return render(request, "encyclopedia/search_results.html", {
    #     "entries": SearchResultsView()
    # })

def page(request, title):
    try:
        mdpage = util.get_entry(title.strip())
        # htmlpage = md.convert(mdpage)
        return render(request, "encyclopedia/page.html", {
            "title": title,
            "content": mdpage
        })
    except:
        return render(request, "encyclopedia/page.html", {
             "content": "Page not found!",
             "title": "Error!"
        })

def add(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"].lower()
            title = title.capitalize()
            text = form.cleaned_data["text"]
            util.save_entry(title, text)
        else:
            return render(request, "encyclopedia/add.html", {
                "form":form
            })

    return render(request, "encyclopedia/add.html", {
        "form" : NewForm()
    })


def random(request):
    entries = util.list_entries()

    juice = entries[randint(0, len(entries)-1)]

    return redirect("page", title=juice.capitalize())

def edit(request, title):
    if request.method == "POST":
        form = NewFormEdit(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            util.save_entry(title, text)
        else:
            return render(request, "encyclopedia/edit.html", {
                "form":form
            })

    return render(request, "encyclopedia/index.html", {
        "form" : NewFormEdit()
    }) 