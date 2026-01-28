from django.shortcuts import render                                                                                                   
import random

quotes = [
    "Be yourself; everyone else is already taken.",
    "To live is the rarest thing in the world. Most people exist, that is all.",
    "Always forgive your enemies; nothing annoys them so much.",
    "We are all in the gutter, but some of us are looking at the stars.",
    "I am so clever that sometimes I don't understand a single word of what I am saying.",
    "The truth is rarely pure and never simple.",
    "You can never be overdressed or overeducated.",
]

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
    context = {
        'quote': random.choice(quotes),
        'image': random.choice(images),
    }
    return render(request, 'quotes/quote.html', context)

def show_all(request):
    context = {
        'quotes': quotes,
        'images': images,
    }
    return render(request, 'quotes/show_all.html', context)

def about(request):
    return render(request, 'quotes/about.html')