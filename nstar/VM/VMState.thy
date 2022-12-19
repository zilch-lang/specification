theory VMState
  imports
    Main
    Instr
    Registers
    Values
begin


type_synonym exec_reg_set = \<open>val reg_set\<close>

type_synonym pc = nat

type_synonym labels = \<open>string \<rightharpoonup> pc\<close>

type_synonym state = \<open>pc option \<times> exec_reg_set \<times> labels\<close>
                   \<comment> \<open>program counter, register states, function IPs\<close>

abbreviation default :: \<open>string \<Rightarrow> (string \<times> pc) list \<Rightarrow> state\<close>
where \<open>default lbl \<Xi> \<equiv> (let \<Xi> = map_of \<Xi> in (\<Xi> lbl, \<emptyset>, \<Xi>))\<close>

end
