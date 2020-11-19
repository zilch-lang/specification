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

inner = Sequence(
    Terminal("section"),
    Terminal("{"),
    OneOrMore(Skip(), NonTerminal('data-entry')),
    Terminal("}")
)

d = Diagram(Start('complex', "data-section"), inner, type="complex", css=MY_STYLE)
d.writeSvg(sys.stdout.write)
