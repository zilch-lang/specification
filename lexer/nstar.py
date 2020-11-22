from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import *


class NStarLexer(RegexLexer):
    name = 'N*'
    aliases = ['nstar']
    filenames = ['*.nst']

    tokens = {
        'commentsandwhitespace': [
            (r'\s+', Text),
            (r'#.*?\n', Comment.Single)
        ],
        'keywords': [
            (r'(forall|unsafe|sptr)\b', Keyword)
        ],
        'literals': [
            (r'"[^"]"', String.Double),
            (r"'[^']'", String.Char),
            (r'0[bB][01]+', Number.Bin),
            (r'0[xX][0-9a-fA-F]+', Number.Hex),
            (r'0[oO][0-7]+', Number.Oct),
            (r'[0-9]+', Number.Integer)
        ],
        'instructions': [
            (r'(ret|mov|jmp|call)\b', Name.Builtin)
        ],
        'registers': [
            (r'(%(rax|rbx|rcx|rdx|rbp|rsp|rdi|rsi))\b', Name.Constant)
        ],
        'root': [
            include('commentsandwhitespace'),
            include('keywords'),
            include('instructions'),
            include('literals'),
            include('registers'),

            (r'(\*|\:\:)', Operator),
            (r'(\{|\}|\.|\:)', Punctuation),

            (r'^([a-zA-Z]*)\:', Name.Variable),
            (r'(Ts|Ta|T4|T8)\b', Keyword.Type),
            (r'.', Text)
        ]
    }
