import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(
        sorted(
            re.sub(r"\.md$", "", filename)
            for filename in filenames
            if filename.endswith(".md")
        )
    )


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def search(title):
    """
    get list of all encyclopedia entries that have the query as a substring.
    or returns the name of the file
    """
    suggestions = list()
    # I don't need the directory
    _, filenames = default_storage.listdir("entries")
    for filename in filenames:
        if filename.endswith(".md"):
            # extract the .md from the entry if any.
            filename = re.sub(r"\.md$", "", filename)
            if title.lower() == filename.lower():
                # file found
                return (True, filename)
            if title.lower() in filename.lower():
                suggestions.append(filename)
    # it returns false and list of suggestions in case we could  not find the right file
    return (False, suggestions)


def is_exist(title):
    _, filenames = default_storage.listdir("entries")
    for filename in filenames:
        if filename.endswith(".md"):
            filename = re.sub(r"\.md$", "", filename)
            if filename == title:
                return True
    return False


def save(title, text):
    try:
        f = default_storage.open(f"entries/{title}.md", "w")
        print(text)
        f.write(str(text.encode("utf-8")))
    except FileNotFoundError:
        pass
