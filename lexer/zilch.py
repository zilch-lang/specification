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
            (r'--.*?$', Comment.Single),
            (r'\/-', Comment.Multi, 'multi')
        ],
        'multi': [
            # support markdown highlighting?
            (r'[^-\/]', Comment.Multi),
            (r'-\/', Comment.Multi, '#pop'),
            (r'[-\/]', Comment.Multi)
        ],
        'keywords': [
            (r'\b(let|rec|effect|enum|record|where|import|as|open|match|with|type|lam|λ|val|constructor|public|mut|region|assume|do|if|then|else|mutual|true|false|resume|unsafe)\b', Keyword.Reserved)
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
            (r'\b(s8|s16|s32|s64|u8|u16|u32|u64|char|ptr|ref|𝟏)\b', Keyword.Type),
            (r'\B(⊤|⊗|&|×|->|→|𝟭|\(\s*\)|⟨\s*⟩)\B', Keyword.Type),
            (r'@[0-9]+', Comment.Preproc)
        ],
        'operators': [
            (r'(\:\=|≔|=>|⇒)', Operator),

            (r'(\(|\)|\:|\{|\})|,|_', Punctuation)
        ],
        'meta-specifier': [
            (r'#attributes\(.*?\)', Comment.Preproc)
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
