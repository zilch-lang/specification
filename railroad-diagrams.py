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

def zilch_lambda():
  inner = Choice(
    0,
    Sequence(
      Terminal('lam'),
      Choice(
        1,
        NonTerminal('identifier'),
        Sequence(
          Terminal('('),
          ZeroOrMore(
            Sequence(
              NonTerminal('identifier'),
              Optional(
                Sequence(
                  Terminal(':'),
                  NonTerminal('type')
                )
              )
            ),
            Terminal(',')
          ),
          Terminal(')')
        )
      ),
      Terminal('->'),
      NonTerminal('{'),
      NonTerminal('expression'),
      NonTerminal('}')
    ),
    Terminal('_')
  )

  return mk_diagram2('lambda', inner)

zilch_lambda().writeSvg(sys.stdout.write)
