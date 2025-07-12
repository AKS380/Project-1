import spacy
from spacy.tokenizer import Tokenizer
from spacy.util import compile_infix_regex, compile_prefix_regex, compile_suffix_regex

def custom_tokenizer_factory(nlp):
    infix_patterns = list(nlp.Defaults.infixes) + [r'\{', r'\}', r'\[', r'\]', r':', r',']
    infix_re = compile_infix_regex(infix_patterns)
    prefix_re = compile_prefix_regex(nlp.Defaults.prefixes)
    suffix_re = compile_suffix_regex(nlp.Defaults.suffixes)

    return Tokenizer(
        nlp.vocab,
        rules=nlp.Defaults.tokenizer_exceptions,
        prefix_search=prefix_re.search,
        suffix_search=suffix_re.search,
        infix_finditer=infix_re.finditer
    )
