from django.utils.text import slugify


def generate_slug(name):
    """
    Generate a slug from a given string.
    """

    return slugify(name)