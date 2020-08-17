import re, os, random
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


def get_random_entryTitle():
    """
    This function returns a  title of a random entry
    """
    return re.sub(r"\.md$", "", random.choice(os.listdir("./entries")))


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
    """
    This wrapper function checks if the file exist or not
    """
    return default_storage.exists(f"entries/{title}.md")


def save(title, text):
    """
    This function is used to save the file.
    """
    f = default_storage.open(f"entries/{title}.md", "wb")
    f.write(text.encode("utf-8"))


def edit(old_title, title, text):
    """
    As it's name implies this function is useful to if we want to edit an entry.
    """
    f = default_storage.open(f"entries/{old_title}.md", "wb")
    f.write(text.encode("utf-8"))
    os.rename(f"entries/{old_title}.md", f"entries/{title}.md")
