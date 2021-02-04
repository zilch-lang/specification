from railroad import *

MY_STYLE = '''\
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

def mk_diagram(name, nodes):
    return Diagram(Start('complex', name), nodes, type='complex', css=MY_STYLE)

def character_immediate():
    inner = Sequence(
		Terminal("'"),
		Choice(
			1,
			Sequence(
				Terminal('\\'),
				Choice(
					1,
					Sequence(
						Terminal('x'),
						NonTerminal('hex-digit'),
						NonTerminal('hex-digit')
					),
					HorizontalChoice(
						Terminal('n'),
						Terminal('r'),
						Terminal('\\'),
						Terminal('0')
					),
					HorizontalChoice(
						Terminal('t'),
						Terminal('v'),
						Terminal('e')
					),
				)
			),
			NonTerminal('ascii-character')
		),
		Terminal("'")
    )

    return mk_diagram('character-immediate', inner)

def character_constant():
    return character_immediate()

def nop_instruction():
	inner = Sequence(
		Terminal('nop')
	)

	return mk_diagram('nop-instruction', inner)

def code_line():
	inner = Stack(
		Sequence(
			Optional(
				Terminal('global')
			),
			NonTerminal('identifier'),
			Terminal(':'),
			NonTerminal('label-type'),
			Terminal('=')
		),
		Choice(
			1,
			NonTerminal('instruction_block'),
			Sequence(
				Terminal('unsafe'),
				Terminal('{'),
				NonTerminal('instruction_block'),
				Terminal('}')
			)
		)
	)

	return mk_diagram('code-line', inner)

def data_section():
	inner = Sequence(
		Terminal('section'),
		Choice(
			1,
			Terminal('data'),
			Terminal('rodata'),
			Terminal('udata')
		),
		Terminal('{'),
		ZeroOrMore(
			Choice(
				1,
				Sequence(
					Optional(
						Terminal('global')
					),
					NonTerminal('identifier'),
					Terminal(':'),
					NonTerminal('constant-type')
				),
				NonTerminal('constant-value')
			)
		),
		Terminal('}')
	)

	return mk_diagram('data-section', inner)

def extern_data_section():
	inner = Sequence(
		Terminal('section'),
		Choice(
			0,
			Terminal('extern.data'),
			Terminal('extern.rodata')
		),
		Terminal('{'),
		ZeroOrMore(
			Sequence(
				Optional(
					Terminal('dyn')
				),
				NonTerminal('identifier'),
				Terminal(':'),
				NonTerminal('constant-type')
			)
		),
		Terminal('}')
	)

	return mk_diagram('extern.data-section', inner)

def label_type():
	inner = Sequence(
		Choice(
			0,
			Terminal('forall'),
			Terminal('∀')
		),
		Terminal('('),
		ZeroOrMore(
			Sequence(
				NonTerminal('identifier'),
				Terminal(':'),
				NonTerminal('kind')
			),
			Terminal(',')
		),
		Terminal(')'),
		Terminal('.'),
		NonTerminal('context-type')
	)

	return mk_diagram('label-type', inner)

def context_type():
	inner = Sequence(
		Terminal('{'),
		ZeroOrMore(
			Sequence(
				NonTerminal('register'),
				Terminal(':'),
				NonTerminal('type')
			),
			Terminal(',')
		),
		Terminal('|'),
		NonTerminal('stack-type'),
		Choice(
			0,
			Terminal('->'),
			Terminal('→')
		),
		NonTerminal('cont-type'),
		Terminal('}')
	)

	return mk_diagram('context-type', inner)

def cont_type():
	inner = Choice(
		1,
		Group(
			NonTerminal('digit'),
			'Stack index'
		),
		Group(
			NonTerminal('identifier'),
			'Type variable'
		),
		Group(
			NonTerminal('register'),
			'Register'
		)
	)

	return mk_diagram('cont-type', inner)

def kind():
	inner = Choice(
		1,
		Terminal('Ta'),
		Terminal('Ts'),
		Terminal('Tc'),
		Sequence(
			Terminal('T'),
			NonTerminal("positive-integer")
		)
	)

	return mk_diagram('kind', inner)

def instruction_block():
	inner = Choice(
		1,
		Sequence(
			Optional(
				Terminal('unsafe')
			),
			NonTerminal('instruction'),
			Terminal(';'),
			NonTerminal('instruction_block')
		),
		Group(
			Choice(
				1,
				NonTerminal('ret-instruction'),
				NonTerminal('call-instruction'),
				NonTerminal('jmp-instruction')
			),
			'Terminal instructions'
		)
	)

	return mk_diagram('instruction-block', inner)

def code_section():
	inner = Sequence(
		Terminal('section'),
		Terminal('code'),
		Terminal('{'),
		ZeroOrMore(
			NonTerminal('code-line')
		),
		Terminal('}')
	)

	return mk_diagram('code-section', inner)

def jmp_instruction():
	inner = Sequence(
		Terminal('jmp'),
		Group(
			NonTerminal('identifier'),
			'target label'
		),
		Group(
			Optional(
				Sequence(
					Terminal('<'),
					ZeroOrMore(
						NonTerminal('type'),
						Terminal(',')
					),
					Terminal('>')
				)
			),
			'type specialisation'
		)
	)

	return mk_diagram('jmp-instruction', inner)

def call_instruction():
	inner = Sequence(
		Terminal('call'),
		Group(
			NonTerminal('identifier'),
			'target label'
		),
		Group(
			Optional(
				Sequence(
					Terminal('<'),
					ZeroOrMore(
						NonTerminal('type'),
						Terminal(',')
					),
					Terminal('>')
				)
			),
			'type specialisation'
		)
	)

	return mk_diagram('call-instruction', inner)

call_instruction().writeSvg(sys.stdout.write)
