from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import *


class ZilchLexer(RegexLexer):
    name = 'Zilch'
    aliases = ['zilch']
    filenames = ['*.z']

    tokens = {
        'commentsandwhitespace': [
            (r'\s+', Text),
            (r'--.*?\n', Comment.Single)
        ],
        'keywords': [
            (r'\b(forall|∀|def|enum|record|class|impl|do|type|case|of|module|fn|foreign|import|export|perm|if|then|else|pattern|where|as)\b', Keyword.Reserved)
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

            (r'(\(|\)|\:|\{|\}|\[|\])|,', Punctuation)
        ],
        'identifier': [
            (r'((?!\d)\S)\S*', Text)
        ],
        'root': [
            include('commentsandwhitespace'),
            include('keywords'),
            include('types'),
            include('operators'),
            include('identifier'),
            include('literals'),

            (r'.', Text)
        ]
    }
