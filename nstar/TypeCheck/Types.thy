theory Types
  imports
    Main
    Registers
begin

datatype kind =
  Ts
| Ta
| Tc
| T nat

type_synonym quantified_vars = \<open>string \<rightharpoonup> kind\<close>

datatype continuation =
  R reg
| V string

datatype type' =
  U nat
| S nat
| Fn quantified_vars \<open>reg \<rightharpoonup> type'\<close> stack continuation

and stack =
  Empty
| Cons type' stack

type_synonym registers = \<open>reg \<rightharpoonup> type'\<close>

end
