from . import util

from django.shortcuts import render
from django import forms


class NewForm(forms.Form):
    title = forms.CharField(label="Title")
    text = forms.CharField(label="Text")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title):
    try:
        mdpage = util.get_entry(title)
        htmlpage = md.convert(mdpage)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": htmlpage
        })
    except:
        return render(request, "encyclopedia/error.html", {
            "error": "Page not found!",
            "title": "Error!"
        })

def add(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            util.save_entry(title, text)
        else:
            return render(request, "encyclopedia/add.html", {
                "form":form
            })

    return render(request, "encyclopedia/add.html", {
        "form" : NewForm()
    })

