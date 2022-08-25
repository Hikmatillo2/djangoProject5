from transliterate.decorators import transliterate_function
import re


@transliterate_function(language_code='ru', reversed=True)
def translit(text):
    alph = set('АаБбВвГгДдЕеЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя1234567890!""@№#$;%^:&*()-=+{}[]`~<>,/'
               '\_')
    diff_set = set(text).difference(alph)
    if re.fullmatch('http.*', text):
        return '_'.join(text.split()).lower()
    elif diff_set:
        for symbol in diff_set:
            text = text.replace(symbol, '')
        return '_'.join(text.split()).lower()
    return '_'.join(text.split()).lower()
