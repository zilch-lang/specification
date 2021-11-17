from pygments.lexer import ExtendedRegexLexer, bygroups, include
from pygments.token import *
import re


class ZilchLexer(ExtendedRegexLexer):
    name = 'Zilch'
    aliases = ['zilch']
    filenames = ['*.z']

    tokens = {
        'commentsandwhitespace': [
            (r'\s+', Text),
            (r'--.*?$', Comment.Single)
        ],
        'keywords': [
            (r'\b(forall|∀|def|enum|record|class|impl|alias|case|of|module|fn|foreign|import|export|perm|if|then|else|pattern|where|as|open|let|in|lam)\b', Keyword.Reserved)
        ],
        'literals': [
            (r'"[^"]*"', String.Double),
            (r"'[^']'", String.Char),
            (r'0[bB][01]+', Number.Bin),
            (r'0[xX][0-9a-fA-F]+', Number.Hex),
            (r'0[oO][0-7]+', Number.Oct),
            (r'[0-9]+', Number.Integer)
        ],
        'types': [
            (r'\b(s8|s16|s32|s64|u8|u16|u32|u64)\b', Keyword.Type)
        ],
        'operators': [
            (r'(\:\=|\<\-|\<\:|←|≔|\-\>|→|·)', Operator),

            (r'(\(|\)|\:|\{|\}|\[|\])|,|_', Punctuation)
        ],
        'meta-specifier': [
            (r'#\[.*?\]', Comment.Preproc)
        ],
        'root': [
            include('commentsandwhitespace'),
            include('keywords'),
            include('meta-specifier'),
            include('types'),
            include('operators'),
            include('literals'),

            (r'.', Text)
        ]
    }
