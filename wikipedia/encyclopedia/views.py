from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entryPage(request, title):
    entry = util.get_entry(title)
    if entry:
        return render(
            request, "encyclopedia/entryPage.html", {"entry": entry, "title": title},
        )
    else:
        # TODO : have to fix  this later
        return HttpResponseNotFound("<h1>Page not found</h1>")
