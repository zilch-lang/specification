theory FullTC
  imports
    Main
    "HOL-Library.Monad_Syntax"
    HOL.Transitive_Closure
    TypeCheck.TCInstr
begin

fun typecheck_all :: \<open>[ tc_lstate, code ] \<Rightarrow> (bool \<times> tc_rstate) option\<close>
where \<open>typecheck_all (_, \<chi>, \<sigma>, \<epsilon>) [] = Some (False, \<chi>, \<sigma>, \<epsilon>)\<close>
    | \<open>typecheck_all (\<Xi>, \<chi>, \<sigma>, \<epsilon>) (i # is) = do {
        (is_terminal, \<chi>', \<sigma>', \<epsilon>') \<leftarrow> typecheck_instr i \<Xi> \<chi> \<sigma> \<epsilon>;
        if is_terminal
          then Some (is_terminal, \<chi>', \<sigma>', \<epsilon>')
          else typecheck_all (\<Xi>, \<chi>', \<sigma>', \<epsilon>') is
      }\<close>

definition typecheck_all' :: \<open>[ tc_lstate, code, tc_rstate ] \<Rightarrow> bool\<close>
  (\<open>_ \<turnstile>ⁱ* _ \<stileturn> _\<close> [91, 91, 91] 90)
where [simp]: \<open>typecheck_all' Ls c Rs \<equiv> typecheck_all Ls c = Some (True, Rs)\<close>

(*****************************************)

lemma program1_typechecks:
  defines \<open>program1 \<equiv> [Move (Vint 3) R0, Move (Vint 4) R1, Halt]\<close>
      and \<open>\<Xi> \<equiv> \<lambda>_. None\<close>
      and \<open>\<chi> \<equiv> \<lambda>_. None\<close>
      and \<open>\<sigma> \<equiv> Empty\<close>
  shows \<open>\<exists> Rs. (\<Xi>, \<chi>, \<sigma>, R R5) \<turnstile>ⁱ* program1 \<stileturn> Rs\<close>
proof -
  have \<open>(\<Xi>, \<chi>, \<sigma>, R R5) \<turnstile>ⁱ Move (Vint 3) R0 \<stileturn> (False, (\<chi>(R0 \<mapsto> U 64), \<sigma>, R R5))\<close>
    by (simp add: TC_move)
  moreover have \<open>(\<Xi>, \<chi>(R0 \<mapsto> U 64), \<sigma>, R R5) \<turnstile>ⁱ Move (Vint 4) R1 \<stileturn> (False, (\<chi>(R0 \<mapsto> U 64)(R1 \<mapsto> U 64), \<sigma>, R R5))\<close>
    by (simp add: TC_move)
  moreover have \<open>(\<Xi>, \<chi>(R0 \<mapsto> U 64)(R1 \<mapsto> U 64), \<sigma>, R R5) \<turnstile>ⁱ Halt \<stileturn> (True, (\<chi>(R0 \<mapsto> U 64)(R1 \<mapsto> U 64), \<sigma>, R R5))\<close>
    by (simp add: TC_halt)
  ultimately have \<open>(\<Xi>, \<chi>, \<sigma>, R R5) \<turnstile>ⁱ* program1 \<stileturn> (\<chi>(R0 \<mapsto> U 64)(R1 \<mapsto> U 64), \<sigma>, R R5)\<close>
    by (simp add: program1_def)
  thus ?thesis
    by auto
qed

end
