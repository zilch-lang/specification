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
            (r'(forall|∀|unsafe)\b', Keyword)
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
            (r'(ret|mv|jmp|call|cmp|je|sfree|salloc|st|sref)\b', Name.Builtin.Pseudo)
        ],
        'registers': [
            (r'(%(r0|r1|r2|r3|r4|r5))\b', Name.Builtin.Pseudo)
        ],
        'types': [
            (r'(Ts|Ta|Tc|T4|T8|s8|s16|s32|s64|u8|u16|u32|u64)\b', Keyword.Type)
        ],
        'variables': [
            (r'^([a-zA-Z_]*)\:', Name.Label),
            (r'(jmp|call|je)( )([a-zA-Z]*)(\<.*?\>)?', bygroups(Name.Builtin.Pseudo, Text, Name.Label, Text))
        ],
        'root': [
            include('commentsandwhitespace'),
            include('keywords'),
            include('variables'),
            include('instructions'),
            include('literals'),
            include('registers'),
            include('types'),

            (r'(\*|\:\:|(\-\>)|\|)', Operator),
            (r'(\{|\}|\.|\:)', Punctuation),

            (r'.', Text)
        ]
    }
