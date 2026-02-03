# File: views.py
# Author: Letitia Caspersen (letitiac@bu.edu), 2/3/2026
# Description: View functions for Sealy's Restaurant web application

from django.shortcuts import render
import random

# List of daily specials
daily_specials = [
    "Grilled Swordfish with Lemon Caper Butter",
    "Pan-Seared Scallops with Sweet Corn Risotto",
    "Miso-Glazed Salmon with Sesame Green Beans",
    "Mussels in White Wine Garlic Broth with Grilled Bread",
    "Coastal Market Catch with Seasonal Vegetables"
]

menu = {
    'clam_chowder': {
        'name': 'New England Clam Chowder',
        'price': 13,
    },
    'lobster_roll': {
        'name': 'Lobster Roll',
        'price': 28,
    },
    'fish_and_chips': {
        'name': 'Fish & Chips',
        'price': 22,
        'options' : ['Tartar Sauce', 'Malt Vinegar', 'Ketchup'],
    },
    'shrimp_scampi': {
        'name': 'Shrimp Scampi',
        'price': 26,
    },
    'crab_cakes': {
        'name': 'Crab Cakes',
        'price': 25,
    },
}

def main(request):
    """Return an HTML page displaying the main Sealy's Restaurant page."""
    return render(request, 'restaurant/main.html')

def order(request):
    """Return an HTML page displaying Sealy's online order form with random daily special."""
    context = {
        'menu' : menu,
        'daily_special': random.choice(daily_specials),
    }
    return render(request, 'restaurant/order.html', context)

def confirmation(request):
    """Process the order form submission and display confirmation page."""

    # Read data from order form
    name = request.POST.get('name', '')
    phone = request.POST.get('phone', '')
    email = request.POST.get('email', '')
    special_instructions = request.POST.get('special_instructions', '')

    # Check which menu items were ordered and calculate total price
    ordered_items = []
    total_price = 0.0
    for item in menu:
        # If request contains menu item, add it to total
        if request.POST.get(item):
            ordered_items.append(item)
            total_price += item['price']

    # Aggregate context for confirmation page
    context = {
        'name': name,
        'phone': phone,
        'email': email,
        'special_instructions': special_instructions,
        'ordered_items': ordered_items,
        'total_price': total_price,
    }
    return render(request, 'restaurant/confirmation.html', context)
