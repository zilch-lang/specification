from railroad import *

NSTAR_STYLE = '''\
  svg.railroad-diagram {
    background-color:rgba(0,0,0,0);
  }
  svg.railroad-diagram path {
    stroke-width:3;
    stroke:black;
    fill:rgba(0,0,0,0);
  }
  svg.railroad-diagram text {
    font:bold 14px monospace;
    text-anchor:middle;
  }
  svg.railroad-diagram text.label{
    text-anchor:start;
  }
  svg.railroad-diagram text.comment{
    font:italic 12px monospace;
  }
  svg.railroad-diagram rect{
    stroke-width:3;
    stroke:black;
    fill:hsl(1,100%,72%);
  }
  svg.railroad-diagram rect.group-box {
    stroke: gray;
    stroke-dasharray: 10 5;
    fill: none;
  }
'''

ZILCH_STYLE = '''\
  svg.railroad-diagram {
    background-color:rgba(0,0,0,0);
  }
  svg.railroad-diagram path {
    stroke-width:3;
    stroke:black;
    fill:rgba(0,0,0,0);
  }
  svg.railroad-diagram text {
    font:bold 14px monospace;
    text-anchor:middle;
  }
  svg.railroad-diagram text.label{
    text-anchor:start;
  }
  svg.railroad-diagram text.comment{
    font:italic 12px monospace;
  }
  svg.railroad-diagram rect{
    stroke-width:3;
    stroke:black;
    fill:hsl(209,73%,55%);
  }
  svg.railroad-diagram rect.group-box {
    stroke: gray;
    stroke-dasharray: 10 5;
    fill: none;
  }
'''


def mk_diagram(name, nodes):
  return Diagram(Start('complex', name),
                 nodes,
                 type='complex',
                 css=NSTAR_STYLE)


def mk_diagram2(name, nodes):
  return Diagram(Start('complex', name),
                 nodes,
                 type='complex',
                 css=ZILCH_STYLE)


def nstar_character_immediate():
  inner = Sequence(Terminal("'"), NonTerminal('string-character'),
                   Terminal("'"))

  return mk_diagram('character-immediate', inner)


def nstar_character_constant():
  return character_immediate()


def nstar_nop_instruction():
  inner = Sequence(Terminal('nop'))

  return mk_diagram('nop-instruction', inner)


def nstar_code_line():
  inner = Sequence(Optional(Terminal('global')), NonTerminal('identifier'),
                   Terminal(':'), NonTerminal('label-type'), Terminal('='),
                   NonTerminal('instruction-block'))

  return mk_diagram('code-line', inner)


def nstar_data_section():
  inner = Sequence(Terminal('section'),
                   Choice(1, Terminal('data'), Terminal('rodata')),
                   Terminal('{'), ZeroOrMore(NonTerminal('data-line')),
                   Terminal('}'))

  return mk_diagram('data-section', inner)


def nstar_extern_data_section():
  inner = Sequence(
    Terminal('section'),
    Choice(0, Terminal('extern.data'), Terminal('extern.rodata')),
    Terminal('{'),
    ZeroOrMore(
      Sequence(Optional(Terminal('dyn')), NonTerminal('identifier'),
               Terminal(':'), NonTerminal('constant-type'))), Terminal('}'))

  return mk_diagram('extern.data-section', inner)


def nstar_label_type():
  inner = Sequence(
    Choice(0, Terminal('forall'), Terminal('∀')), Terminal('('),
    ZeroOrMore(
      Sequence(NonTerminal('identifier'), Terminal(':'), NonTerminal('kind')),
      Terminal(',')), Terminal(')'), Terminal('.'),
    NonTerminal('context-type'))

  return mk_diagram('label-type', inner)


def nstar_context_type():
  inner = Sequence(
    Terminal('{'),
    ZeroOrMore(
      Sequence(NonTerminal('register'), Terminal(':'), NonTerminal('type')),
      Terminal(',')), Terminal('|'), NonTerminal('stack-type'),
    Choice(0, Terminal('->'), Terminal('→')), NonTerminal('cont-type'),
    Terminal('}'))

  return mk_diagram('context-type', inner)


def nstar_cont_type():
  inner = Choice(1, Group(NonTerminal('positive-integer'), 'Stack index'),
                 Group(NonTerminal('identifier'), 'Type variable'),
                 Group(NonTerminal('register'), 'Register'))

  return mk_diagram('cont-type', inner)


def nstar_kind():
  inner = Choice(1, Terminal('Ta'), Terminal('Ts'), Terminal('Tc'),
                 Sequence(Terminal('T'), NonTerminal("positive-integer")))

  return mk_diagram('kind', inner)


def nstar_instruction_block():
  inner = Choice(
    1,
    Sequence(Optional(Terminal('unsafe')), NonTerminal('instruction'),
             Terminal(';'), NonTerminal('instruction_block')),
    Group(
      Choice(1,
             NonTerminal('ret-instruction'), NonTerminal('call-instruction'),
             NonTerminal('jmp-instruction')), 'Terminal instructions'))

  return mk_diagram('instruction-block', inner)


def nstar_code_section():
  inner = Sequence(Terminal('section'), Terminal('code'), Terminal('{'),
                   ZeroOrMore(NonTerminal('code-line')), Terminal('}'))

  return mk_diagram('code-section', inner)


def nstar_jmp_instruction():
  inner = Sequence(Terminal('jmp'),
                   Group(NonTerminal('label-specialization'), 'target label'))

  return mk_diagram('jmp-instruction', inner)


def nstar_call_instruction():
  inner = Sequence(Terminal('call'),
                   Group(NonTerminal('label-specialization'), 'target label'))

  return mk_diagram('call-instruction', inner)


def nstar_ptr_byte_offset():
  inner = Sequence(
    Group(
      Choice(1, Comment('0'), NonTerminal('register'),
             NonTerminal('signed-integer')), 'offset'), Terminal('('),
    Group(
      Choice(
        1, NonTerminal('register'), NonTerminal('label'),
        Group(
          Sequence(Terminal('$'),
                   NonTerminal('positive-integer'), Terminal(':'),
                   NonTerminal('type')), 'typed memory address')), 'source'),
    Terminal(')'))

  return mk_diagram('pointer-byte-offset', inner)


def nstar_ptr_offset():
  inner = Sequence(
    Group(Choice(1, NonTerminal('register'), NonTerminal('label')), 'source'),
    Terminal('['),
    Group(Choice(1, NonTerminal('register'), NonTerminal('signed-integer')),
          'offset'), Terminal(']'))

  return mk_diagram('pointer-offset', inner)


def nstar_label_specialization():
  inner = Sequence(
    NonTerminal('identifier'),
    Optional(
      Sequence(Terminal('<'), ZeroOrMore(NonTerminal('type'), Terminal(',')),
               Terminal('>'))))

  return mk_diagram('label-value', inner)


def nstar_register():
  inner = Sequence(
    Terminal('%'),
    Choice(0, HorizontalChoice(Terminal('r0'), Terminal('r1'), Terminal('r2')),
           HorizontalChoice(Terminal('r3'), Terminal('r4'), Terminal('r5'))))

  return mk_diagram('register', inner)


def nstar_udata_section():
  inner = Sequence(Terminal('section'), Terminal('udata'), Terminal('{'),
                   ZeroOrMore(NonTerminal('udata-line')), Terminal('}'))

  return mk_diagram('udata-section', inner)


def nstar_data_line():
  inner = Sequence(Optional(Terminal('global')), NonTerminal('identifier'),
                   Terminal(':'), NonTerminal('constant-type'), Terminal('='),
                   NonTerminal('constant-value'))

  return mk_diagram('data-line', inner)


def nstar_udata_line():
  inner = Sequence(Optional(Terminal('global')), NonTerminal('identifier'),
                   Terminal(':'), NonTerminal('constant-type'))

  return mk_diagram('udata-line', inner)


def nstar_mv_instruction():
  inner = Sequence(
    Terminal('mv'),
    Group(
      Choice(1, NonTerminal('label-value'), NonTerminal('register'),
             NonTerminal('integer-value')), 'source'), Terminal(','),
    Group(NonTerminal('register'), 'destination'))

  return mk_diagram('mv-instruction', inner)


def nstar_sst_instruction():
  inner = Sequence(
    Terminal('sst'),
    Group(Choice(0, NonTerminal('register'), NonTerminal('integer-value')),
          'source'), Terminal(','),
    Group(NonTerminal('positive-integer'), 'stack index destination'))

  return mk_diagram('sst-instruction', inner)


def nstar_sld_instruction():
  inner = Sequence(
    Terminal('sld'),
    Group(NonTerminal('positive-integer'), 'stack index source'),
    Terminal(','), Group(NonTerminal('register'), 'destination'))

  return mk_diagram('sld-instruction', inner)


def nstar_st_instruction():
  inner = Sequence(
    Terminal('st'),
    Group(Choice(0, NonTerminal('register'), NonTerminal('integer-value')),
          'source'), Terminal(','),
    Group(NonTerminal('pointer-offset'), 'destination'))

  return mk_diagram('st-instruction', inner)


def nstar_ld_instruction():
  inner = Sequence(Terminal('ld'),
                   Group(NonTerminal('pointer-offset'),
                         'source'), Terminal(','),
                   Group(NonTerminal('register'), 'destination'))

  return mk_diagram('ld-instruction', inner)


def nstar_sfree_instruction():
  inner = Sequence(Terminal('sfree'))

  return mk_diagram('sfree-instruction', inner)


def nstar_salloc_instruction():
  inner = Sequence(Terminal('salloc'), NonTerminal('type'))

  return mk_diagram('salloc-instruction', inner)


def nstar_include_section():
  inner = Sequence(
    Terminal('include'), Terminal('{'),
    ZeroOrMore(Sequence(Terminal('"'), NonTerminal('file-path'),
                        Terminal('"'))), Terminal('}'))

  return mk_diagram('include-section', inner)


def nstar_bang_type():
  inner = Sequence(Terminal('!'))

  return mk_diagram('bang-type', inner)


def nstar_string_constant():
  inner = Sequence(Terminal("\""), ZeroOrMore(NonTerminal('string-character')),
                   Terminal("\""))

  return mk_diagram('string-constant', inner)


def nstar_sref_instruction():
  inner = Sequence(Terminal('sref'), NonTerminal('positive-integer'),
                   Terminal(','), NonTerminal('register'))

  return mk_diagram('sref-instruction', inner)


def nstar_string_character():
  inner = Choice(
    1,
    Sequence(
      Terminal('\\'),
      Choice(
        1,
        Sequence(Terminal('x'), NonTerminal('hex-digit'),
                 NonTerminal('hex-digit')),
        HorizontalChoice(Terminal('n'), Terminal('r'), Terminal('\\'),
                         Terminal('0')),
        HorizontalChoice(Terminal('t'), Terminal('v'), Terminal('e')),
      )), NonTerminal('ascii-character'))

  return mk_diagram('string-character', inner)


def nstar_struct_constant():
  inner = Sequence(
    Terminal('('),
    ZeroOrMore(
      Choice(1, NonTerminal('integer-value'), NonTerminal('character-value'),
             NonTerminal('structure-constant')), Terminal(',')), Terminal(')'))

  return mk_diagram('structure-constant', inner)


##################################################################################""


def zilch_function_definition():
  inner = Stack(
    Sequence(
      NonTerminal('function-declaration'),
      Optional(
        Sequence(Choice(0, Terminal(':='), Terminal('≔')),
                 NonTerminal('expression')))))

  return mk_diagram2('function-definition', inner)


def zilch_toplevel_function_definition():
  inner = Sequence(
    NonTerminal('function-definition'),
    Optional(
      Sequence(Terminal('where'), NonTerminal('{'),
               OneOrMore(NonTerminal('function-definition'), NonTerminal(';')),
               NonTerminal('}'))))

  return mk_diagram2('toplevel-function-definition', inner)


def zilch_identifier():
  inner = Choice(
    0,
    Group(
      Sequence(NonTerminal('alpha'), ZeroOrMore(NonTerminal('alphanumeric'))),
      '∉ keywords'),
    Sequence(Terminal('('), NonTerminal('symbol'), Terminal(')')))

  return mk_diagram2('identifier', inner)


def zilch_keywords():
  inner = Choice(
    1,
    HorizontalChoice(Terminal('forall'), Terminal('∀'), Terminal('enum'),
                     Terminal('record'), Terminal('class'), Terminal('impl'),
                     Terminal('where'), Terminal('rec')),
    HorizontalChoice(Terminal('alias'), Terminal('case'), Terminal('of'),
                     Terminal('module'), Terminal('foreign'), Terminal('as'),
                     Terminal('open'), Terminal('import')),
    HorizontalChoice(Terminal('export'), Terminal('effect'), Terminal('if'),
                     Terminal('then'), Terminal('else'), Terminal('pattern'),
                     Terminal('let'), Terminal('in')),
    HorizontalChoice(Terminal(':='), Terminal('->'), Terminal('→'),
                     Terminal('≔'), Terminal('_'), Terminal('·'),
                     Terminal('.'), Terminal('--'), Terminal('?'),
                     Terminal(':')))

  return mk_diagram2('keywords', inner)


def zilch_special():
  inner = HorizontalChoice(Terminal('('), Terminal(')'), Terminal('['),
                           Terminal(']'), Terminal('{'), Terminal('}'),
                           Terminal(','), Terminal('_'), Terminal('·'))

  return mk_diagram2('special', inner)


def zilch_whitespaces():
  inner = OneOrMore(
    Choice(
      1, NonTerminal('any invisible character'),
      Sequence(Terminal('--'), ZeroOrMore(NonTerminal('any character')),
               Terminal('end of line'))))

  return mk_diagram2('whitespaces', inner)


def zilch_number():
  inner = Choice(
    2,
    Group(
      Sequence(Terminal('0'), HorizontalChoice(Terminal('b'), Terminal('B')),
               OneOrMore(NonTerminal('binary digit'))),
      'binary integer literal'),
    Group(
      Sequence(Terminal('0'), HorizontalChoice(Terminal('o'), Terminal('O')),
               OneOrMore(NonTerminal('octal digit'))),
      'octal integer literal'),
    Group(
      Sequence(Terminal('0'), HorizontalChoice(Terminal('x'), Terminal('X')),
               OneOrMore(NonTerminal('hexadecimal digit'))),
      'hexadecimal integer literal'),
    Group(
      Sequence(OneOrMore(NonTerminal('decimal digit')), Terminal('.'),
               OneOrMore(NonTerminal('decimal digit'))),
      'floating point literal'),
    Group(OneOrMore(NonTerminal('decimal digit')), 'decimal integer literal'))

  return mk_diagram2('number', inner)


def zilch_string():
  inner = Sequence(
    Terminal('"'),
    ZeroOrMore(
      Choice(1, NonTerminal('any espace sequence'),
             Group(NonTerminal('any character'), '≠ "'))), Terminal('"'))

  return mk_diagram2('string', inner)


def zilch_character():
  inner = Sequence(
    Terminal("'"),
    Choice(1, NonTerminal('any escape sequence'),
           Group(NonTerminal('any character'), "≠ '")), Terminal("'"))

  return mk_diagram2('character', inner)


def zilch_lambda():
  inner = Choice(
    1, HorizontalChoice(Terminal('·'), Terminal('_')),
    Sequence(
      Choice(
        0, NonTerminal('identifier'),
        Sequence(
          Terminal('('),
          ZeroOrMore(
            Sequence(NonTerminal('identifier'),
                     Optional(Sequence(Terminal(':'), NonTerminal('type')))),
            Terminal(',')), Terminal(')'))),
      Choice(0, Terminal('->'), Terminal('→')), NonTerminal('expression')))

  return mk_diagram2('lambda', inner)


def zilch_conditional():
  inner = Sequence(Terminal('if'), NonTerminal('expression'), Terminal('then'),
                   NonTerminal('expression'), Terminal('else'),
                   NonTerminal('expression'))

  return mk_diagram2('conditional', inner)


def zilch_do():
  inner = Sequence(
    Terminal('do'), NonTerminal('{'),
    Optional(
      Sequence(
        OneOrMore(
          Choice(
            1,
            Sequence(NonTerminal('identifier'),
                     HorizontalChoice(Terminal('<-'), Terminal('←')),
                     NonTerminal('expression')), NonTerminal('expression')),
          NonTerminal(';')), NonTerminal(';'))), NonTerminal('expression'),
    NonTerminal('}'))

  return mk_diagram2('do', inner)


def zilch_case():
  inner = Sequence(
    Terminal('case'), NonTerminal('expression'), Terminal('of'),
    NonTerminal('{'),
    OneOrMore(
      Sequence(NonTerminal('pattern'),
               HorizontalChoice(Terminal('->'), Terminal('→')),
               NonTerminal('expression')), NonTerminal(';')), NonTerminal('}'))

  return mk_diagram2('case', inner)


def zilch_record():
  inner = Sequence(
    Terminal('{'),
    ZeroOrMore(
      Sequence(NonTerminal('identifier'),
               HorizontalChoice(Terminal(':='), Terminal('≔')),
               NonTerminal('expression')), Terminal(',')), Terminal('}'))

  return mk_diagram2('record', inner)


def zilch_basicexpr():
  inner = Choice(
    3, NonTerminal('literal'), Group(NonTerminal('identifier'), 'variable'),
    Group(
      Sequence(NonTerminal('expression'), Terminal('('),
               ZeroOrMore(NonTerminal('expression')), Terminal(')')),
      'function application'),
    Group(
      Sequence(NonTerminal('expression'), Terminal('.'),
               NonTerminal('identifier')), 'record/module access'),
    Group(Terminal('?'), 'typed hole'),
    Group(Sequence(Terminal('('), NonTerminal('expression'), Terminal(')')),
          'parenthesized expression'),
    Group(
      Sequence(NonTerminal('expression'), NonTerminal('symbol'),
               NonTerminal('expression')), 'infix operator application'))

  return mk_diagram2('expression-atom', inner)


def zilch_pattern():
  inner = Choice(
    2, NonTerminal('any non-string literal'),
    HorizontalChoice(Terminal('·'), Terminal('_')),
    Group(
      Sequence(
        NonTerminal('identifier'),
        Sequence(Terminal('('),
                 ZeroOrMore(NonTerminal('pattern'), Terminal(',')),
                 Terminal(')'))), 'enum constructor'),
    Group(
      Sequence(NonTerminal('pattern'), NonTerminal('symbol'),
               NonTerminal('pattern')), 'infix pattern synonym'))

  return mk_diagram2('pattern', inner)


def zilch_mixfix():
  inner = Sequence(
    Optional(NonTerminal('identifier')),
    OneOrMore(NonTerminal('expression'), NonTerminal('identifier')),
    Optional(NonTerminal('identifier')))

  return mk_diagram2('mixfix', inner)


def zilch_type():
  inner = Stack(
    Sequence(
      Terminal('alias'), NonTerminal('identifier'),
      Optional(
        Sequence(
          Terminal('('),
          ZeroOrMore(
            Sequence(NonTerminal('identifier'),
                     Optional(Sequence(Terminal(':'), NonTerminal('kind')))),
            Terminal(',')), Terminal(')')))),
    Sequence(Choice(0, Terminal(':='), Terminal('≔')), NonTerminal('type')))

  return mk_diagram2('type-alias', inner)


def zilch_enum():
  inner = Stack(
    Sequence(
      Terminal('enum'), NonTerminal('identifier'),
      Optional(
        Sequence(
          Terminal('('),
          ZeroOrMore(
            Sequence(NonTerminal('identifier'),
                     Optional(Sequence(Terminal(':'), NonTerminal('kind')))),
            Terminal(',')), Terminal(')')))),
    Sequence(
      Choice(0, Terminal(':='), Terminal('≔')), NonTerminal('{'),
      ZeroOrMore(
        Sequence(NonTerminal('identifier'), NonTerminal('('),
                 ZeroOrMore(NonTerminal('type'), Terminal(',')),
                 NonTerminal(')')), NonTerminal(';')), NonTerminal('}')))

  return mk_diagram2('enum', inner)


def zilch_record():
  inner = Stack(
    Sequence(
      Terminal('record'), NonTerminal('identifier'),
      Optional(
        Sequence(
          Terminal('('),
          ZeroOrMore(
            Sequence(NonTerminal('identifier'),
                     Optional(Sequence(Terminal(':'), NonTerminal('kind')))),
            Terminal(',')), Terminal(')')))),
    Sequence(
      Choice(0, Terminal(':='), Terminal('≔')), NonTerminal('{'),
      ZeroOrMore(
        Sequence(NonTerminal('identifier'), Terminal(':'),
                 NonTerminal('type')), NonTerminal(';')), NonTerminal('}')))

  return mk_diagram2('record', inner)


def zilch_function_declaration():
  inner = Stack(
    Sequence(
      Terminal('let'),
      Optional(
        Sequence(
          Terminal('<'),
          ZeroOrMore(
            Choice(
              0, NonTerminal('identifier'),
              Sequence(OneOrMore(NonTerminal('identifier')),
                       Sequence(Terminal(':'), NonTerminal('kind')))),
            Terminal(',')),
          Optional(
            Sequence(Terminal('|'),
                     OneOrMore(NonTerminal('type'), Terminal(',')))),
          Terminal('>')))),
    Sequence(
      NonTerminal('identifier'),
      Optional(
        Sequence(
          Terminal('('),
          ZeroOrMore(
            Sequence(NonTerminal('identifier'),
                     Optional(Sequence(Terminal(':'), NonTerminal('type')))),
            Terminal(',')), Terminal(')'))),
      Optional(Sequence(Terminal(':'), NonTerminal('type')))))

  return mk_diagram2('function-declaration', inner)


def zilch_typeclass():
  inner = Stack(
    Sequence(
      Terminal('class'), NonTerminal('identifier'), Terminal('('),
      ZeroOrMore(
        Sequence(NonTerminal('identifier'), Terminal(':'),
                 NonTerminal('kind')), Terminal(',')), Terminal(')')),
    Sequence(
      Optional(
        Sequence(Terminal('|'), OneOrMore(NonTerminal('type'),
                                          Terminal(',')))),
      Choice(0, Terminal(':='), Terminal('≔')), NonTerminal('{'),
      ZeroOrMore(
        Sequence(NonTerminal('identifier'), Terminal(':'),
                 NonTerminal('type')), NonTerminal(';')), NonTerminal('}')))

  return mk_diagram2('type-class', inner)


def zilch_impl():
  inner = Stack(
    Sequence(
      Terminal('impl'),
      Optional(
        Sequence(
          Terminal('<'),
          ZeroOrMore(NonTerminal('identifier'),
                     Optional(Sequence(Terminal(':'), NonTerminal('kind')))),
          Optional(
            Sequence(Terminal('|'),
                     OneOrMore(NonTerminal('type'), Terminal(',')))),
          Terminal('>')))),
    Sequence(NonTerminal('identifier'), Terminal(':'),
             NonTerminal('identifier'), Terminal('('),
             ZeroOrMore(NonTerminal('type'), Terminal(',')), Terminal(')')),
    Sequence(
      Choice(0, Terminal(':='), Terminal('≔')), NonTerminal('{'),
      ZeroOrMore(NonTerminal('toplevel-function-definition'),
                 NonTerminal(';')), NonTerminal('}')))

  return mk_diagram2('type-class-impl', inner)


def zilch_fixity():
  inner = Sequence(
    Choice(1, Terminal('infixl'), Terminal('infix'), Terminal('infixr')),
    NonTerminal('positive-integer'), NonTerminal('identifier'))

  return mk_diagram2('fixity-declaration', inner)


def zilch_forall_type():
  inner = Sequence(HorizontalChoice(Terminal('forall'), Terminal('∀')),
                   NonTerminal('forall-quantification'), NonTerminal('type'))

  return mk_diagram2('forall-type', inner)


def zilch_constrained_type():
  inner = Sequence(Terminal('['), ZeroOrMore(NonTerminal('type'),
                                             Terminal(',')), Terminal(']'),
                   NonTerminal('type'))

  return mk_diagram2('constrained-type', inner)


def zilch_function_type():
  inner = Sequence(
    Choice(
      1, NonTerminal('atom-type'),
      Sequence(
        Terminal('('),
        ZeroOrMore(NonTerminal('type'), Terminal(',')),
        Terminal(')'),
      )), Optional(NonTerminal('effect-row')),
    Choice(0, Terminal('->'), Terminal('→')), NonTerminal('type'))

  return mk_diagram2('function-type', inner)


def zilch_application_type():
  inner = Sequence(
    Choice(
      0,
      Sequence(
        Terminal('('),
        ZeroOrMore(NonTerminal('type'), Terminal(',')),
        Terminal(')'),
      ),
      NonTerminal('atom-type'),
    ), Optional(NonTerminal('effect-row')),
    HorizontalChoice(Terminal('->'), Terminal('→')), NonTerminal('type'))

  return mk_diagram2('type-application', inner)


def zilch_builtin_types():
  inner = Choice(
    1,
    HorizontalChoice(Terminal('s8'), Terminal('s16'), Terminal('s32'),
                     Terminal('s64')),
    HorizontalChoice(Terminal('u8'), Terminal('u16'), Terminal('u32'),
                     Terminal('u64')),
    HorizontalChoice(Terminal('char'), Terminal('ref'), Terminal('ptr')))

  return mk_diagram2('builtin-type', inner)


def zilch_wildcard_type():
  inner = HorizontalChoice(Terminal('·'), Terminal('_'))

  return mk_diagram2('wildcard-type', inner)


def zilch_effect_type():
  inner = Sequence(
    NonTerminal('identifier'),
    ZeroOrMore(Sequence(Terminal('|'), NonTerminal('effect-type'))))

  return mk_diagram2('effect-type', inner)


def zilch_kind():
  inner = Choice(
    1, Terminal('type'),
    Group(
      Sequence(
        Choice(
          0, NonTerminal('kind'),
          Sequence(
            Terminal('('),
            ZeroOrMore(NonTerminal('kind'), Terminal(',')),
            Terminal(')'),
          )), HorizontalChoice(Terminal('->'), Terminal('→')),
        NonTerminal('kind')), 'type-level function'))

  return mk_diagram2('atom-kind', inner)


def zilch_module_header():
  inner = Sequence(
    Terminal('export'), Terminal('('),
    ZeroOrMore(
      Sequence(
        Choice(1, Terminal('module'), Skip(), Terminal('type'),
               Terminal('effect')),
        OneOrMore(NonTerminal('identifier'), Terminal('.'))), Terminal(',')),
    Terminal(')'))

  return mk_diagram2('module-header', inner)


def zilch_module_import():
  inner = Stack(
    Sequence(
      Optional(Terminal('open')),
      Terminal('import'),
      OneOrMore(NonTerminal('identifier'), Terminal('.')),
    ),
    Sequence(
      Optional(
        Sequence(
          Terminal('('),
          ZeroOrMore(
            Sequence(
              Choice(1, Terminal('type'), Skip(), Terminal('effect'),
                     Terminal('module')), NonTerminal('identifier'),
              Optional(Sequence(Terminal('as'), NonTerminal('identifier')))),
            Terminal(',')), Terminal(')')))))

  return mk_diagram2('module-import', inner)


def zilch_meta_information():
  inner = Sequence(Terminal('#['),
                   ZeroOrMore(NonTerminal('meta-specifier'), Terminal(',')),
                   Terminal(']'))

  return mk_diagram2('meta-information', inner)


def zilch_meta_specifier():
  inner = Choice(
    1,
    Sequence(Terminal('foreign'),
             Choice(0, Terminal('export'), Terminal('import'))),
    Sequence(
      Choice(1, Terminal('infix'), Terminal('infixl'), Terminal('infixr')),
      NonTerminal('positive-integer')), Terminal('inline'))

  return mk_diagram2('meta-specifier', inner)


def zilch_symbol():
  inner = Group(
    Sequence(Group(NonTerminal('symbol'), '∉ special'),
             ZeroOrMore(Group(NonTerminal('symbol'), '∉ special'))),
    '∉ keywords')

  return mk_diagram2('symbol', inner)


def zilch_letin():
  inner = Stack(
    Sequence(OneOrMore(NonTerminal('function-definition')), Terminal('in'),
             NonTerminal('expression')))

  return mk_diagram2('let-in', inner)


def zilch_forall_quantification():
  inner = Sequence(
    Terminal('<'),
    Group(
      ZeroOrMore(
        Choice(
          1,
          Sequence(OneOrMore(NonTerminal('identifier')), Terminal(':'),
                   NonTerminal('type')), NonTerminal('identifier')),
        Terminal(',')), 'parameters'),
    Optional(
      Sequence(
        Terminal('|'),
        Group(OneOrMore(NonTerminal('type'), Terminal(',')), 'constraints'))),
    Terminal('>'))

  return mk_diagram2('forall-quantification', inner)


def zilch_effect_handler():
  inner = Stack(
    Sequence(Terminal('handler'), NonTerminal('identifier'),
             Optional(NonTerminal('forall-quantification'))),
    Sequence(Terminal('('), zilch_parameters(NonTerminal('type')),
             Terminal(')')),
    Sequence(HorizontalChoice(Terminal(':='), Terminal('≔')), NonTerminal('{'),
             OneOrMore(NonTerminal('effect-handler-branch'), NonTerminal(';')),
             NonTerminal('}')))

  return mk_diagram2('effect-handler', inner)


def zilch_parameters(ty):
  return ZeroOrMore(
    Choice(1, Sequence(OneOrMore(NonTerminal('identifier')), Terminal(':'),
                       ty), NonTerminal('identifier')), Terminal(','))


def zilch_effect_handler_branch():
  inner = Sequence(
    Choice(
      0,
      Sequence(
        Terminal('return'),
        Choice(2, NonTerminal('identifier'), Terminal('_'), Terminal('·')),
      ),
      Sequence(
        NonTerminal('identifier'), Terminal('('),
        ZeroOrMore(
          Choice(1, NonTerminal('identifier'), Terminal('_'), Terminal('·')),
          Terminal(',')), Terminal(')'))),
    HorizontalChoice(Terminal('->'), Terminal('→')), NonTerminal('expression'))

  return mk_diagram2('effect-handler-branch', inner)


def zilch_effect_row():
  inner = Sequence(
    Terminal('{'), ZeroOrMore(NonTerminal('type'), Terminal(',')),
    Optional(
      Sequence(Terminal('|'),
               OneOrMore(NonTerminal('identifier'), Terminal(',')))),
    Terminal('}'))

  return mk_diagram2('effect-row', inner)


zilch_forall_quantification().writeSvg(sys.stdout.write)
