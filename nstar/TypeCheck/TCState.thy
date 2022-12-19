theory TCState
  imports
    Main
    Registers
    Instr
    Values
    TypeCheck.Types
begin

type_synonym labels = \<open>string \<rightharpoonup> type'\<close>

type_synonym tc_rstate = \<open>registers \<times> stack \<times> continuation\<close>
                    \<comment> \<open>register mapping, current stack, current continuation\<close>

type_synonym tc_lstate = \<open>labels \<times> registers \<times> stack \<times> continuation\<close>

end
