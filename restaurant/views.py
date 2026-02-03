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

# Menu items with prices 
menu_prices = {
    'clam_chowder': 13,
    'lobster_roll': 28,
    'fish_and_chips': 22,
    'shrimp_scampi': 26,
    'crab_cakes': 25,
    'daily_special': 33,
}

# Menu items display names
menu_names = {
        'clam_chowder': 'New England Clam Chowder',
        'lobster_roll': 'Lobster Roll',
        'fish_and_chips': 'Fish & Chips',
        'shrimp_scampi': 'Shrimp Scampi',
        'crab_cakes': 'Crab Cakes',
        'daily_special': 'Daily Special',
    }

def main(request):
    """Return an HTML page displaying the main Sealy's Restaurant page."""
    return render(request, 'restaurant/main.html')

def order(request):
    """Return an HTML page displaying Sealy's online order form with random daily special."""
    context = {
        'menu' : menu_prices,
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
    for item, price in menu_prices.items():

        # If request contains menu item, add it to total
        if request.POST.get(item):
            ordered_items.append({
                'name': menu_names[item],
                'price': price,
            })
            total_price += price

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
