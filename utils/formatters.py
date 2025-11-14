def format_currency(amount):
    """Formatear moneda en pesos argentinos"""
    return f"$ {amount:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')