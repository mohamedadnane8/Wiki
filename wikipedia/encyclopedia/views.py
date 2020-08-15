from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from . import util
from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(label="")


def index(request):
    return render(
        request,
        "encyclopedia/index.html",
        {"entries": util.list_entries(), "form": SearchForm()},
    )


def entryPage(request, title):
    entry = util.get_entry(title)
    if entry:
        return render(
            request,
            "encyclopedia/entryPage.html",
            {"entry": entry, "title": title, "form": SearchForm()},
        )
    else:
        # TODO : have to fix  this later
        return render(request, "encyclopedia/404.html", {"form": SearchForm()})


def search(request):

    # Check if method is POST
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = SearchForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the task from the 'cleaned' version of form data
            keyWord = form.cleaned_data["search"]
            # Redirect user to list of tasks
            # Search How to redirect!
            is_entry, ans = util.search(keyWord)
            print(is_entry)
            if is_entry:
                return render(
                    request,
                    "encyclopedia/entryPage.html",
                    {
                        "form": SearchForm(),
                        "title": keyWord,
                        "entry": util.get_entry(keyWord),
                    },
                )
            else:
                return render(
                    request,
                    "encyclopedia/search.html",
                    {"entries": ans, "form": SearchForm(), "keyWord": keyWord},
                )
        else:
            # If the form is invalid, re-render the page with existing information.
            return index(request)
    return index(request)
