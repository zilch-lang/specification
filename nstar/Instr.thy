theory Instr
  imports
    Main
    Registers Values
begin

datatype instr =
  Move val reg
| Halt
| Jump string

type_synonym code = \<open>instr list\<close>

end
