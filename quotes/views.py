# File: views.py
# Author: Letitia Caspersen (letitiac@bu.edu), 1/28/2026
# Description: Quotes and images of Oscar Wilde with random selection 
# functionality to support Oscar Wilde quotes webapp

from django.shortcuts import render                                                                                                   
import random

# List of Oscar Wilde quotes
quotes = [
    "Be yourself; everyone else is already taken.",
    "To live is the rarest thing in the world. Most people exist, that is all.",
    "Always forgive your enemies; nothing annoys them so much.",
    "We are all in the gutter, but some of us are looking at the stars.",
    "I am so clever that sometimes I don't understand a single word of what I am saying.",
    "The truth is rarely pure and never simple.",
    "You can never be overdressed or overeducated.",
]

# List of paths to Oscar Wilde images, images are stored in static folder
images = [
    'quotes/oscar1.jpg',                                                                                                              
    'quotes/oscar2.jpg',                                                                                                              
    'quotes/oscar3.jpg',                                                                                                              
    'quotes/oscar4.jpg',                                                                                                              
    'quotes/oscar5.jpg',                                                                                                              
    'quotes/oscar6.jpg',                                                                                                              
    'quotes/oscar7.jpg',                                                                                                              
    'quotes/oscar8.jpg',                                                                                                              
    'quotes/oscar9.jpg',
]

def quote(request):
    """Return an HTML page displaying a random quote and image."""
    context = {
        'quote': random.choice(quotes),
        'image': random.choice(images),
    }
    return render(request, 'quotes/quote.html', context)


def show_all(request):
    """Return an HTML page displaying all quotes and images."""
    context = {
        'quotes': quotes,
        'images': images,
    }
    return render(request, 'quotes/show_all.html', context)

def about(request):
    """Return an HTML page displaying the about section."""
    return render(request, 'quotes/about.html')