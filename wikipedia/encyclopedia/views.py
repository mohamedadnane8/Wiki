from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from . import util, entryForms


def index(request):
    return render(
        request,
        "encyclopedia/index.html",
        {"entries": util.list_entries(), "form": entryForms.SearchForm()},
    )


def entryPage(request, title):
    entry = util.get_entry(title)
    if title:
        return render(
            request,
            "encyclopedia/entryPage.html",
            {"entry": entry, "title": title, "form": entryForms.SearchForm()},
        )
    else:
        # TODO : have to fix  this later
        return render(
            request, "encyclopedia/404.html", {"form": entryForms.SearchForm()}
        )


def searchEntry(request):
    if request.method == "POST":
        form = entryForms.SearchForm(request.POST)

        if form.is_valid():
            # Isolate the task from the 'cleaned' version of form data
            keyWord = form.cleaned_data["search"]

            is_entry, ans = util.search(keyWord)
            print(is_entry)
            if is_entry:
                return redirect("encyclopedia:entry", title=keyWord)
            else:
                return render(
                    request,
                    "encyclopedia/search.html",
                    {
                        "entries": ans,
                        "form": entryForms.SearchForm(),
                        "keyWord": keyWord,
                    },
                )
        else:
            if is_entry:
                return redirect("encyclopedia:index")


def create(request):
    if request.method == "POST":

        form = entryForms.CreateForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            print(title)
            if util.is_exist(title):
                return render(
                    request, "encyclopedia/404.html", {"form": entryForms.SearchForm()}
                )
            util.save(title, content)
            return redirect("encyclopedia:entry", title=title)
    return render(
        request,
        "encyclopedia/create.html",
        {"form": entryForms.SearchForm(), "createform": entryForms.CreateForm()},
    )


def edit(request, title):
    # in case a post request was sent.
    # we will save the file once again and redirect to the entry page.
    print("\n\n\n yeess mmmeennn")

    if request.method == "POST":
        form = entryForms.CreateForm(request.POST)

        if form.is_valid():
            print(title)

            new_content = form.cleaned_data["content"]
            new_title = form.cleaned_data["title"]

            util.edit(title, new_title, new_content)
            return redirect("encyclopedia:entry", title=new_title)

    # this is not post request, so we will render the page.
    entry = util.get_entry(title)
    if title:
        form = entryForms.CreateForm()
        form = entryForms.CreateForm({"content": entry, "title": title,})
        return render(
            request,
            "encyclopedia/edit.html",
            {
                "form": entryForms.SearchForm(),
                "createform": form,
                "title": title,
                "entry": entry,
            },
        )
