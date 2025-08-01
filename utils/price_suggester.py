def suggest_prices(current_price):
    """
    Suggest a list of lower prices for user to choose for alerts.
    Based on percentage drops from the current price.
    """
    suggestions = []

    # Suggest 10% to 40% drops in steps
    for percent in [10, 20, 30, 40]:
        drop_price = current_price - int((percent / 100) * current_price)
        if drop_price > 0:
            suggestions.append(drop_price)

    # Remove duplicates and sort in descending order
    suggestions = sorted(list(set(suggestions)), reverse=True)
    return suggestions
