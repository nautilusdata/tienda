from django import template

register = template.Library()

@register.filter(name='numberFormat')
def numberFormat(numero):
    """
    Formatea un número con separadores de miles para su visualización.
    Ejemplo: 1234567 se convierte en 1.234.567
    """
    if numero is None:
        return 0
    else:
        # Formatea el número con separadores de miles y reemplaza la coma por un punto.
        # Esto es útil para la convención de formato de números en español.
        return "{:,.0f}".format(numero).replace(",", ".")