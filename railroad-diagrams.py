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


def nstar_cj_triadic():
  inner = Sequence(
    Terminal('cjX'),
    Choice(0, NonTerminal('register'), NonTerminal('integer-value')),
    Terminal(','), NonTerminal('label-value'), Terminal(','),
    NonTerminal('label-value'))

  return mk_diagram('triadic-cjX', inner)


def nstar_cj_tetradic():
  inner = Sequence(
    Terminal('cjC'),
    Choice(0, NonTerminal('register'), NonTerminal('integer-value')),
    Terminal(','),
    Choice(0, NonTerminal('register'), NonTerminal('integer-value')),
    Terminal(','), NonTerminal('label-value'), Terminal(','),
    NonTerminal('label-value'))

  return mk_diagram('tetradic-cjC', inner)


def nstar_shiftX_instruction():
  inner = Sequence(
    Terminal('shiftX'),
    Choice(0, NonTerminal('register'), NonTerminal('integer-value')),
    Terminal(','), NonTerminal('integer-value'), Terminal(','),
    NonTerminal('register'))

  return mk_diagram('shiftX-instruction', inner)


def nstar_logical_unary_instruction():
  inner = Sequence(
    Choice(0, Terminal('not')),
    Choice(0, NonTerminal('register'), NonTerminal('integer-value')),
    Terminal(','), NonTerminal('register'))

  return mk_diagram('logical-unary-instruction', inner)


def nstar_logical_binary_instruction():
  inner = Sequence(
    Choice(1, Terminal('and'), Terminal('or'), Terminal('xor')),
    Choice(0, NonTerminal('register'), NonTerminal('integer-value')),
    Terminal(','),
    Choice(0, NonTerminal('register'), NonTerminal('integer-value')),
    Terminal(','), NonTerminal('register'))

  return mk_diagram('logical-binary-instruction', inner)


def nstar_cmvZ_quaternary_instruction():
  inner = Sequence(
    Choice(0, Terminal('cmvz'), Terminal('cmvnz')),
    Choice(0, NonTerminal('register'), NonTerminal('integer-value')),
    Terminal(','), NonTerminal('register'), Terminal(','),
    NonTerminal('register'), Terminal(','), NonTerminal('register'))

  return mk_diagram('cmvZ-instruction', inner)


def nstar_cmvX_quaternary_instruction():
  inner = Sequence(
    Choice(2, Terminal('cmve'), Terminal('cmvne'), Terminal('cmvl'),
           Terminal('cmvle'), Terminal('cmvg'), Terminal('cmvge')),
    Choice(0, NonTerminal('register'), NonTerminal('integer-value')),
    Terminal(','), NonTerminal('register'), Terminal(','),
    NonTerminal('register'), Terminal(','), NonTerminal('register'))

  return mk_diagram('cmvX-instruction', inner)


def nstar_iarithmetic_instruction():
  inner = Sequence(
    Choice(1, Terminal('add'), Terminal('sub'), Terminal('mul'),
           Terminal('div')),
    Choice(0, NonTerminal('register'), NonTerminal('integer-value')),
    Terminal(','),
    Choice(0, NonTerminal('register'), NonTerminal('integer-value')),
    Terminal(','), NonTerminal('register'))

  return mk_diagram('iarithmetic-instruction', inner)


##################################################################################
## Zilch
##################################################################################


def zilch_keywords():
  inner = Choice(
    2,
    Group(
      HorizontalChoice(Terminal('import'), Terminal('as'), Terminal('open')),
      'module-level'),
    Group(
      Choice(
        1,
        HorizontalChoice(Terminal('open'), Terminal('public'), Terminal('let'),
                         Terminal('rec'), Terminal('val'), Terminal('mut')),
        HorizontalChoice(Terminal('enum'), Terminal('record'),
                         Terminal('effect'), Terminal('constructor')),
        HorizontalChoice(Terminal('mutual'), Terminal('assume'))),
      'top-level'),
    Group(HorizontalChoice(Terminal('type'), Terminal('region')),
          'type-level'),
    Group(
      Choice(
        1,
        HorizontalChoice(Terminal('match'), Terminal('with'), Terminal('lam'),
                         Terminal('where'), Terminal('λ')),
        HorizontalChoice(Terminal('if'), Terminal('then'), Terminal('else'),
                         Terminal('do'), Terminal('true'), Terminal('false')),
        HorizontalChoice(Terminal('resume'), Terminal('unsafe'))),
      'expression-level'))

  return mk_diagram2('keywords', inner)


def zilch_identifier():
  inner = Group(
    Sequence(Group(NonTerminal('any'), '∉ digit'),
             ZeroOrMore(NonTerminal('any'))), '∉ keywords')

  return mk_diagram2('identifier', inner)


def zilch_special():
  inner = Choice(
    1,
    HorizontalChoice(Terminal('('), Terminal(')'), Terminal('{'),
                     Terminal('}'), Terminal('{{'), Terminal('}}'),
                     Terminal('⦃'), Terminal('⦄')),
    HorizontalChoice(Terminal(':='), Terminal('≔'), Terminal(','),
                     Terminal(':'), Terminal('::'), Terminal('∷'),
                     Terminal('->'), Terminal('→')),
    HorizontalChoice(Terminal('--'), Terminal('/-'), Terminal('-/'),
                     Terminal('/--'), Terminal('_'), Terminal('·'),
                     Terminal('?'), Terminal('=>'), Terminal('⇒')))

  return mk_diagram2('special', inner)


def zilch_whitespaces():
  inner = OneOrMore(
    Choice(
      1, NonTerminal('any invisible character'),
      Group(
        Sequence(Terminal('--'), ZeroOrMore(NonTerminal('any character')),
                 Terminal('end of line')), 'inline comment'),
      Group(
        Sequence(HorizontalChoice(Terminal('/-'), Terminal('/--')),
                 ZeroOrMore(NonTerminal('any character')), Terminal('-/')),
        'multiline comment')))

  return mk_diagram2('whitespaces', inner)


def zilch_lambda():
  inner = Sequence(
    Choice(0, Terminal('lam'), Terminal('λ')),
    OneOrMore(
      Choice(2, Sequence(Terminal('('), Terminal(')')),
             NonTerminal('explicit-parameter'),
             NonTerminal('implicit-parameter'),
             NonTerminal('instance-parameter'))),
    Choice(0, Terminal('=>'), Terminal('⇒')), NonTerminal('{'),
    NonTerminal('expression'), NonTerminal('}'))

  return mk_diagram2('lambda', inner)


def zilch_integer():
  inner = Choice(
    2,
    Group(
      Sequence(Terminal('0'), HorizontalChoice(Terminal('x'), Terminal('X')),
               OneOrMore(NonTerminal('hex-digit'))), 'hexadecimal'),
    Group(
      Sequence(Terminal('0'), HorizontalChoice(Terminal('b'), Terminal('B')),
               OneOrMore(NonTerminal('bin-digit'))), 'binary'),
    Group(
      Sequence(Terminal('0'), HorizontalChoice(Terminal('o'), Terminal('O')),
               OneOrMore(NonTerminal('oct-digit'))), 'octal'),
    Group(
      Sequence(NonTerminal('dec-digit'), Terminal('.'),
               NonTerminal('dec-digit')), 'floating point'),
    Group(OneOrMore('dec-digit'), 'decimal'))

  return mk_diagram2('integer', inner)


def zilch_dependent_type():
  inner = Sequence(
    Choice(1, Sequence(Optional(NonTerminal('usage')),
                       NonTerminal('type-atom')),
           OneOrMore(NonTerminal('explicit-parameter')),
           OneOrMore(NonTerminal('implicit-parameter')),
           OneOrMore(NonTerminal('instance-parameter'))),
    Choice(
      2,
      Terminal('⊗'),
      Terminal('×'),
      Terminal('->'),
      Terminal('→'),
      Terminal('&'),
    ), Optional(NonTerminal('effect-row')), NonTerminal('type'))

  return mk_diagram2('dependent-type', inner)


def zilch_implicit_parameter():
  inner = Sequence(
    Terminal('{'),
    OneOrMore(
      Sequence(
        Optional(NonTerminal('usage')),
        Choice(
          1,
          Sequence(OneOrMore(NonTerminal('identifier')), Terminal(':'),
                   NonTerminal('type')), NonTerminal('type-atom'))),
      Terminal(',')), Terminal('}'))

  return mk_diagram2('implicit-parameter', inner)


def zilch_implicit_parameter_():
  inner = Sequence(
    Terminal('{'),
    OneOrMore(
      Sequence(
        Optional(NonTerminal('usage')),
        Choice(
          1,
          Sequence(OneOrMore(NonTerminal('identifier')), Terminal(':'),
                   NonTerminal('expression')), NonTerminal('identifier'))),
      Terminal(',')), Terminal('}'))

  return mk_diagram2('implicit-parameter\'', inner)


def zilch_explicit_parameter():
  inner = Sequence(
    Terminal('('),
    OneOrMore(
      Sequence(
        Optional(NonTerminal('usage')),
        Choice(
          1,
          Sequence(OneOrMore(NonTerminal('identifier')), Terminal(':'),
                   NonTerminal('type')), NonTerminal('type-atom')),
      ), Terminal(',')), Terminal(')'))

  return mk_diagram2('explicit-parameter', inner)


def zilch_explicit_parameter_():
  inner = Sequence(
    Terminal('('),
    OneOrMore(
      Sequence(
        Optional(NonTerminal('usage')),
        Choice(
          1,
          Sequence(OneOrMore(NonTerminal('identifier')), Terminal(':'),
                   NonTerminal('type')), NonTerminal('identifier')),
      ), Terminal(',')), Terminal(')'))

  return mk_diagram2('explicit-parameter\'', inner)


def zilch_instance_parameter():
  inner = Choice(
    0,
    Sequence(Terminal('{{'), Optional(NonTerminal('usage')),
             NonTerminal('identifier'), Terminal(':'), NonTerminal('type'),
             Terminal('}}')),
    Sequence(Terminal('⦃'), Optional(NonTerminal('usage')),
             NonTerminal('identifier'), Terminal(':'), NonTerminal('type'),
             Terminal('⦄')))

  return mk_diagram2('instance-parameter', inner)


def zilch_instance_parameter_():
  inner = Choice(
    0,
    Sequence(Terminal('{{'), Optional(NonTerminal('usage')),
             NonTerminal('identifier'), Terminal(':'), NonTerminal('type'),
             Terminal('}}')),
    Sequence(Terminal('⦃'), Optional(NonTerminal('usage')),
             NonTerminal('identifier'), Terminal(':'), NonTerminal('type'),
             Terminal('⦄')))

  return mk_diagram2('instance-parameter\'', inner)


def zilch_function_type():
  inner = Sequence(
    Choice(
      1, NonTerminal('atomic-type'),
      Sequence(Terminal('('), ZeroOrMore(NonTerminal('type'), Terminal(',')),
               Terminal(')'))), HorizontalChoice(Terminal('->'),
                                                 Terminal('→')),
    Choice(1, Skip(), NonTerminal('identifier'), NonTerminal('effect-row')),
    NonTerminal('type'))

  return mk_diagram2('function-type', inner)


def zilch_effect_row():
  row = Sequence(
    ZeroOrMore(NonTerminal('expression-atom'), Terminal(',')),
    Optional(
      Sequence(Terminal('|'),
               OneOrMore(NonTerminal('identifier'), Terminal(',')))))

  inner = Choice(0, Sequence(Terminal('<'), row, Terminal('>')),
                 Sequence(Terminal('⟨'), row, Terminal('⟩')))

  return mk_diagram2('effect-row', inner)


def zilch_import():
  inner = Stack(
    Sequence(Optional(Terminal('open')), Terminal('import'),
             OneOrMore(NonTerminal('identifier'), Terminal('::'))),
    Sequence(
      Optional(Sequence(Terminal('as'), NonTerminal('identifier'))),
      Optional(
        Sequence(Terminal('('), NonTerminal('module-import-group'),
                 Terminal(')')))))

  return mk_diagram2('module-import', inner)


def zilch_import_group():
  inner = ZeroOrMore(
    Sequence(
      Choice(2, Terminal('class'), Terminal('impl'), Terminal('effect'),
             Skip()), NonTerminal('identifier'),
      Optional(Sequence(Terminal('as'), NonTerminal('identifier')))),
    Terminal(','))

  return mk_diagram2('module-import-group', inner)


def zilch_expression_atom():
  inner = Choice(
    2, NonTerminal('literal'),
    Group(
      Sequence(NonTerminal('expression'),
               HorizontalChoice(Terminal('::'), Terminal('∷')),
               NonTerminal('identifier')), 'qualified identifier'),
    Group(
      Sequence(NonTerminal('expression'), Terminal('('),
               ZeroOrMore(NonTerminal('expression'), Terminal(',')),
               Terminal(')')), 'function application'),
    Group(Sequence(Terminal('('), NonTerminal('expression'), Terminal(')')),
          'parenthesized expression'),
    Group(
      Sequence(NonTerminal('expression'), NonTerminal('symbol'),
               NonTerminal('expression')), 'infix operator application'))

  return mk_diagram2('expression-atom', inner)


def zilch_let_top_level():
  inner = Sequence(
    NonTerminal('function-definition'),
    Optional(
      Sequence(Terminal('where'), NonTerminal('{'),
               OneOrMore(NonTerminal('function-definition'), NonTerminal(';')),
               NonTerminal('}'))))

  return mk_diagram2('toplevel-function', inner)


def zilch_function_definition():
  inner = Stack(
    Sequence(
      Choice(1, Terminal('let'), Terminal('rec'), Terminal('mut')),
      Optional(NonTerminal('usage')), NonTerminal('identifier'),
      ZeroOrMore(
        Choice(1, NonTerminal('explicit-parameter\''),
               NonTerminal('implicit-parameter\''),
               NonTerminal('instance-parameter\'')))),
    Sequence(Optional(Sequence(Terminal(':'), NonTerminal('expression'))),
             Choice(1, Terminal(':='), Terminal('≔')),
             NonTerminal('expression')))

  return mk_diagram2('function-definition', inner)


def zilch_param():
  param = Choice(
    0,
    Sequence(Optional(Choice(0, Terminal('open'), Terminal('mut'))),
             NonTerminal('id'),
             Optional(Sequence(Terminal(':'), NonTerminal('type')))),
    Sequence(OneOrMore(NonTerminal('id')), Terminal(':'), NonTerminal('type')))

  inner = Choice(
    1, Group(Sequence(Terminal('{'), param, Terminal('}')), 'implicit'),
    Group(Sequence(Terminal('('), param, Terminal(')')), 'explicit'),
    Group(
      Sequence(Terminal('{{'), NonTerminal('id'), Terminal(':'),
               NonTerminal('type'), Terminal('}}')), 'instance record'))

  return mk_diagram2('parameter', inner)


def zilch_let_in():
  inner = Sequence(NonTerminal('function-definition'), NonTerminal(';'),
                   NonTerminal('expression'))

  return mk_diagram2('let-in', inner)


def zilch_match():
  inner = Sequence(
    Terminal('match'), NonTerminal('expression'), Terminal('with'),
    NonTerminal('{'),
    OneOrMore(
      Sequence(NonTerminal('pattern'), Choice(1, Terminal('=>'),
                                              Terminal('⇒')),
               NonTerminal('expression')), NonTerminal(';')), NonTerminal('}'))

  return mk_diagram2('match', inner)


def zilch_record():
  record = ZeroOrMore(NonTerminal('function-definition'), Terminal(','))

  inner = Sequence(Terminal('@{'), record, Terminal('}'))

  return mk_diagram2('record', inner)


def zilch_toplevel_enum():
  inner = Stack(
    Sequence(
      Terminal('enum'), NonTerminal('identifier'),
      ZeroOrMore(
        Choice(1, NonTerminal('explicit-parameter\''),
               NonTerminal('implicit-parameter\''),
               NonTerminal('instance-parameter\''))), Terminal(':'),
      NonTerminal('expression')),
    Sequence(Choice(0, Terminal(':='), Terminal('≔')), NonTerminal('{'),
             ZeroOrMore(NonTerminal('function-declaration'), NonTerminal(';')),
             NonTerminal('}')))

  return mk_diagram2('enum', inner)


def zilch_toplevel_record():
  inner = Stack(
    Sequence(
      Terminal('record'), NonTerminal('identifier'),
      ZeroOrMore(
        Choice(1, NonTerminal('explicit-parameter\''),
               NonTerminal('implicit-parameter\''),
               NonTerminal('instance-parameter\''))), Terminal(':'),
      NonTerminal('expression')),
    Sequence(
      Choice(0, Terminal(':='), Terminal('≔')), NonTerminal('{'),
      Optional(
        Sequence(Terminal('constructor'), NonTerminal('identifier'),
                 NonTerminal(';'))),
      ZeroOrMore(NonTerminal('function-declaration'), NonTerminal(';')),
      NonTerminal('}')))

  return mk_diagram2('record', inner)


def zilch_toplevel_function_definition():
  inner = Stack(
    Sequence(Optional(NonTerminal('meta-information')),
             Optional(Terminal('public')), NonTerminal('function-definition')),
    Optional(
      Sequence(Terminal('where'), NonTerminal('{'),
               OneOrMore(NonTerminal('function-definition'), NonTerminal(';')),
               NonTerminal('}'))))

  return mk_diagram2('toplevel-function', inner)


def zilch_function_declaration():
  inner = Sequence(
    Terminal('val'), Optional(NonTerminal('usage')), NonTerminal('identifier'),
    ZeroOrMore(
      Choice(1, NonTerminal('explicit-parameter\''),
             NonTerminal('implicit-parameter\''),
             NonTerminal('instance-parameter\''))), Terminal(':'),
    NonTerminal('expression'))

  return mk_diagram2('function-declaration', inner)


def zilch_mutual_definition():
  inner = Sequence(
    Terminal('mutual'), NonTerminal('{'),
    OneOrMore(NonTerminal('toplevel-definition'), NonTerminal(';')),
    NonTerminal('}'))

  return mk_diagram2('mutual-block', inner)


def zilch_toplevel():
  inner = Sequence(
    Optional(NonTerminal('meta-attributes')), Optional(Terminal('public')),
    Choice(2, NonTerminal('toplevel-function'), NonTerminal('enum'),
           NonTerminal('record'), NonTerminal('function-declaration'),
           NonTerminal('mutual-block')))

  return mk_diagram2('toplevel-definition', inner)


zilch_toplevel().writeSvg(sys.stdout.write)
