from pygments.lexer import ExtendedRegexLexer, bygroups, include
from pygments.token import *
import re


class ZilchLexer(ExtendedRegexLexer):
    name = 'Zilch'
    aliases = ['zilch']
    filenames = ['*.z']

    def identifier_callback(lexer, match, ctx):
        id = match.group(1) + match.group(2)

        if len(parts := id.split("--", 1)) > 1:
            # we might have a comment in here, but it's not sure yet
            if not re.match(r'[^_·]$', parts[0]) and not re.match(r'^[^_·]', parts[1]):
                endofline = ''
                pos = match.start() + len(parts[0])
                while (c := ctx.text[pos]) != '\n':
                    endofline += c
                    pos += 1
                parts[1] = endofline

                yield match.start(), Text, parts[0]
                yield match.start() + len(parts[0]), Comment.Single, parts[1]
                ctx.pos = pos
            else:
                yield match.start(), Text, id
                ctx.pos = match.end()
        else:
            yield match.start(), Text, id
            ctx.pos = match.end()

    tokens = {
        'commentsandwhitespace': [
            (r'\s+', Text),
            (r'--.*?$', Comment.Single)
        ],
        'keywords': [
            (r'\b(forall|∀|def|enum|record|class|impl|do|type|case|of|module|fn|foreign|import|export|perm|if|then|else|pattern|where|as|open)\b', Keyword.Reserved)
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
        'identifier': [
            (r'((?!\d)\S)(\S*)', identifier_callback)
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
            include('identifier'),
            include('literals'),

            (r'.', Text)
        ]
    }
