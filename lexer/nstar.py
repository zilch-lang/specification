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
            (r'(ret|mov|jmp|call|cmp|je)\b', Name.Builtin)
        ],
        'registers': [
            (r'(%(rax|rbx|rcx|rdx|rbp|rsp|rdi|rsi))\b', Name.Constant)
        ],
        'types': [
            (r'(Ts|Ta|T4|T8|s8|s16|s32|s64|u8|u16|u32|u64)\b', Keyword.Type)
        ],
        'variables': [
            (r'^([a-zA-Z]*)\:', Name.Variable),
            (r'(jmp|call|je)( )([a-zA-Z]*)(\<.*?\>)?', bygroups(Keyword, Text, Name.Variable, Text))
        ],
        'root': [
            include('commentsandwhitespace'),
            include('keywords'),
            include('variables'),
            include('instructions'),
            include('literals'),
            include('registers'),
            include('types'),

            (r'(\*|\:\:)', Operator),
            (r'(\{|\}|\.|\:)', Punctuation),

            (r'.', Text)
        ]
    }
