from django import template


register = template.Library()
BANNED_WORDS = [
    'редиска',
    'редиску',
    'редиске',
    'редиска!',


]


@register.filter()
def censor(text):
    """
    """
    check_text = text.lower().split(' ')
    for i in range(len(check_text)):
        if check_text[i] in BANNED_WORDS:
            check_text[i] = ''.join('*' * len(check_text[i]))

    text = ' '.join(check_text).capitalize()
    return f'{text}'
