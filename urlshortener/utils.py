from django.conf import settings
from random import choice
from string import ascii_letters, digits


# Try to get the value from the settings module
SIZE = getattr(settings, 'MAXIMUM_URL_CHARS', 7)
AVAIABLE_CHARS = ascii_letters + digits    # get chars and number

def create_random_code(chars=AVAIABLE_CHARS):
    #  Creates a random string with the predetermined size
    create_str = "".join([choice(chars) for _ in range(SIZE)])
    return create_str

def create_shortened_url(model_instance):
    random_code = create_random_code()
    #  get the moddel class = class Shortener in models.py
    model_class = model_instance.__class__
    list_short_urls =  model_class.objects.filter(shorten_url= random_code)
    if list_short_urls.exists():
        # run the func again
        return create_shortened_url(model_instance)
    return random_code

