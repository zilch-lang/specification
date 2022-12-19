theory TCInstr
  imports
    Main
    "HOL-Library.Monad_Syntax"
    Instr
    Registers
    Values
    HOL.Map
    TypeCheck.TCState
begin

fun typecheck_value :: \<open>[ labels, registers, stack, continuation, val ] \<Rightarrow> type' option\<close>
  (\<open>'(_, _, _, _') \<turnstile>ᶜ _\<close>)
where \<open>typecheck_value _ \<chi> _ _ (Vreg r) = \<chi> r\<close>
    | \<open>typecheck_value _ _ _ _ (Vint _) = Some (U 64)\<close>

fun check_continuation_is_not :: \<open>[ reg, continuation ] \<Rightarrow> unit option\<close>
where \<open>check_continuation_is_not r1 (R r2) = (if r1 = r2 then None else Some ())\<close>
    | \<open>check_continuation_is_not _ _ = Some ()\<close>

primrec typecheck_instr :: \<open>[ instr, labels, registers, stack, continuation ] \<Rightarrow> (bool \<times> tc_rstate) option\<close>
where TC_halt: \<open>typecheck_instr Halt _ \<chi> \<sigma> \<epsilon> = Some (True, \<chi>, \<sigma>, \<epsilon>)\<close>
    | TC_jump: \<open>typecheck_instr (Jump _) _ \<chi> \<sigma> \<epsilon> = None\<close>
    | TC_move: \<open>typecheck_instr (Move v r) \<Xi> \<chi> \<sigma> \<epsilon> = do {
                    check_continuation_is_not r \<epsilon>;
                    \<tau> \<leftarrow> (\<Xi>, \<chi>, \<sigma>, \<epsilon>) \<turnstile>ᶜ v;
                    case (v, \<epsilon>) of
                      (Vreg d, R s) \<Rightarrow>
                        (if d = s
                          then Some (False, \<chi>(r \<mapsto> \<tau>) |` (dom \<chi> - {d}), \<sigma>, R d)
                          else Some (False, \<chi>(r \<mapsto> \<tau>), \<sigma>, \<epsilon>))
                    | _ \<Rightarrow> Some (False, \<chi>(r \<mapsto> \<tau>), \<sigma>, \<epsilon>)
                }\<close>

syntax
  "_typecheck_instr" :: \<open>[ labels, registers, stack, continuation, instr ] \<Rightarrow> (bool \<times> tc_rstate) option\<close>
    (\<open>'(_, _, _, _') \<turnstile>ⁱ _\<close>)
translations
  "(\<Xi>, \<chi>, \<sigma>, \<epsilon>) \<turnstile>ⁱ i" \<rightleftharpoons> "CONST typecheck_instr i \<Xi> \<chi> \<sigma> \<epsilon>"

definition typecheck_instr' :: \<open>[ labels \<times> registers \<times> stack \<times> continuation, instr, bool, tc_rstate ] \<Rightarrow> bool\<close>
  (\<open>_ \<turnstile>ⁱ _ \<stileturn> '(_, _')\<close>)
where [simp]: \<open>typecheck_instr' Lctx i term Rctx \<equiv>
                let (\<Xi>, \<chi>, \<sigma>, \<epsilon>) = Lctx
                 in typecheck_instr i \<Xi> \<chi> \<sigma> \<epsilon> = Some (term, Rctx)\<close>

end
