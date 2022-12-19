theory FullExec
  imports
    Main
    HOL.Transitive_Closure
    HOL.Option
    VM.VMState
    VM.ExecInstr
begin

fun exec :: \<open>code \<Rightarrow> state \<Rightarrow> state option\<close>
where \<open>exec _ (None, _, _) = None\<close>
    | \<open>exec code (Some pc, regs, fns) = Some (exec_instr pc (code ! pc) regs fns)\<close>

definition exec_all :: \<open>[code, state, state] \<Rightarrow> bool\<close>
           (\<open>_ \<turnstile> _ \<leadsto> _\<close> [61, 61, 61] 60)
where \<open>I \<turnstile> s \<leadsto> t \<equiv> (s, t) \<in> {(s, t). exec I s = Some t}\<^sup>+\<close>

(********************************************************)

theorem exec_deterministic: \<open>exec C s = a \<Longrightarrow> exec C s = b \<Longrightarrow> a = b\<close>
  by blast

(* lemma exec_stuck: \<open>exec C (Some pc, \<chi>, \<Xi>) = Some (Some pc, \<chi>, \<Xi>) \<longleftrightarrow> (\<exists>l. C ! pc = Jump l \<and> \<Xi> l = Some pc)\<close>
  oops *)

lemma vm_step1: \<open>C \<turnstile> s \<leadsto> t \<Longrightarrow> exec C s = Some t \<or> (\<exists>z. exec C s = Some z \<and> C \<turnstile> z \<leadsto> t)\<close>
  unfolding exec_all_def
  by (metis (mono_tags, lifting) case_prodD converse_tranclE mem_Collect_eq)

lemma vm_step2: \<open>(\<exists>z. exec C s = Some z \<and> C \<turnstile> z \<leadsto> t) \<longrightarrow> C \<turnstile> s \<leadsto> t\<close>
  unfolding exec_all_def
  by (metis (mono_tags, lifting) case_prodI mem_Collect_eq trancl_into_trancl2)

theorem vm_stuck: \<open>C \<turnstile> s \<leadsto> s \<longleftrightarrow> (\<exists>z. exec C s = Some z \<and> C \<turnstile> z \<leadsto> s)\<close>
  using vm_step1 vm_step2
  by blast

lemma vm_lift: \<open>exec C s = Some t \<Longrightarrow> C \<turnstile> s \<leadsto> t\<close>
  by (simp add: exec_all_def r_into_trancl')

theorem vm_induct [consumes 1, case_names base step, induct pred: exec_all]:
  assumes a: \<open>C \<turnstile> a \<leadsto> b\<close>
      and cases:
        \<open>\<And>x. exec C a = Some x \<Longrightarrow> P x\<close>
        \<open>\<And>y z. C \<turnstile> a \<leadsto> y \<Longrightarrow> exec C y = Some z \<Longrightarrow> P y \<Longrightarrow> P z\<close>
  shows \<open>P b\<close>
  using a
  unfolding exec_all_def
  by (induction x\<equiv>a b) (simp add: cases exec_all_def)+

theorem vm_trans:
  assumes \<open>C \<turnstile> s \<leadsto> a\<close>
      and \<open>C \<turnstile> a \<leadsto> t\<close>
  shows \<open>C \<turnstile> s \<leadsto> t\<close>
  using assms exec_all_def
  by auto

lemma vm_step_trans: \<open>exec C s = Some a \<Longrightarrow> C \<turnstile> s \<leadsto> b \<Longrightarrow> (a = b \<or> C \<turnstile> a \<leadsto> b)\<close>
  by (metis option.inject vm_step1)

theorem no_exec_from_terminal: \<open>exec C s = None \<Longrightarrow> C \<turnstile> s \<leadsto> t \<Longrightarrow> False\<close>
  by (metis option.distinct(1) vm_step1)

(***********************************************)

lemma test1:
  defines \<open>st \<equiv> default ''main'' [(''main'', 0)]\<close>
      and \<open>C \<equiv> [Jump ''main'']\<close>
  shows \<open>C \<turnstile> st \<leadsto> st\<close>
  unfolding st_def C_def exec_all_def
  by auto

(* value \<open>
  let st = default ''main'' [(''main'' , 0)]
  in
    [Jump ''main'', Halt]
    \<turnstile> st
    \<leadsto> st'
\<close> *)

end
