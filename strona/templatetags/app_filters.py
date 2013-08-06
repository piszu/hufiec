from django import template
register = template.Library()

@register.filter
def subtraction( value, arg ):
    '''
    Divides the value; argument is the divisor.
    Returns empty string on any error.
    '''
    try:
        value = long( value )
        arg = long( arg )
        return long( value - arg )
    except: pass
    return 'blad wyliczenia'
