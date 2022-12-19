theory Equivalences
  imports
    Main
    VM.FullExec
    VM.ExecInstr
begin

\<comment> \<open>Let's just ignore all this for now...\<close>

text \<open>

\<close>
lemma vm_diamond:
  assumes \<open>C \<turnstile> s \<leadsto> t1\<close> \<open>C \<turnstile> s \<leadsto> t2\<close>
  shows \<open>\<exists>x. C \<turnstile> t1 \<leadsto> x \<and> C \<turnstile> t2 \<leadsto> x\<close>
  using assms
  sorry

lemma vm_det_induct2 [consumes 2, case_names one_step multi_step]:
  assumes a: \<open>C \<turnstile> s \<leadsto> t1\<close>
      and b: \<open>C \<turnstile> s \<leadsto> t2\<close>
      and one_step: \<open>\<And>x y. exec C s = Some x \<Longrightarrow> exec C s = Some y \<Longrightarrow> P x y\<close>
      and multi_step: \<open>\<And>y1 y2 z1 z2. \<lbrakk> C \<turnstile> s \<leadsto> y1; exec C y1 = Some z1; C \<turnstile> s \<leadsto> y2; exec C y2 = Some z2; P y1 y2 \<rbrakk> \<Longrightarrow> P z1 z2\<close>
  shows \<open>P t1 t2\<close>
  using a b
proof induction
  case (base a1)

  show ?case
    using base.prems base.hyps
  proof induction
    case (base a2)
    thus ?case
      by (simp add: one_step)
  next
    case (step b2 c2)

    have \<open>exec C a1 = Some a1\<close>
      sorry
    thus ?case
      using step.prems step.hyps step.IH multi_step [of a1 a1 b2 c2]
      using vm_lift
      by blast
  qed
next
  case (step b1 c1)

  show ?case
    using step.prems step.hyps step.IH
  proof induction
    case (base a2)

    have \<open>exec C a2 = Some a2\<close>
      sorry
    thus ?case
      using base.prems base.hyps multi_step [of b1 c1 a2 a2]
      using vm_lift
      by blast
  next
    case (step b2 c2)

    have \<open>P b1 b2\<close>
      sorry
    thus ?case
      using step.prems step.hyps step.IH multi_step [of b1 c1 b2 c2]
      by blast
  qed
qed
(* proof (induction rule: vm_induct)
  case (base x1)

  show ?case
    using base.prems base.hyps
  proof (induction rule: vm_induct)
    case (base x2)
    thus ?case
      using one_step
      by blast
  next
    case (step y2 z2)
    thus ?case
      using one_step multi_step
      sorry
  qed
next
  case (step y1 z1)

  show ?case
    using step.prems step.hyps
  proof (induction rule: vm_induct)
    case (base x2)
    thus ?case
      sorry
  next
    case (step y2 z2)
    thus ?case
      sorry
  qed
qed *)

theorem vm_deterministic:
  fixes C :: code
    and s t1 t2 :: state
  assumes \<open>C \<turnstile> s \<leadsto> t1\<close> \<open>C \<turnstile> s \<leadsto> t2\<close>
  shows \<open>t1 = t2\<close>
  using assms
  by (induction rule: vm_det_induct2) simp_all

(*
proof (induction rule: vm_induct)
  case (base x1)

  show ?case
    using base.prems base.hyps
  proof (induction rule: vm_induct)
    case (base x2)
    thus ?case
      by simp
  next
    case (step y2 z2)

    have \<open>x1 = y2 \<or> C \<turnstile> x1 \<leadsto> y2\<close>
      using vm_step_trans step.hyps(1) step.prems(1)
      by blast

    thus ?case
    proof (rule disjE)
      assume *: \<open>x1 = y2\<close>
      hence \<open>C \<turnstile> s \<leadsto> z2\<close>
        using step.hyps vm_lift vm_trans
        by blast
      thus ?thesis
        using step.prems step.hyps
        unfolding *
        (* by (rule vm_deterministic) *)
        sorry
    next
      assume \<open>C \<turnstile> x1 \<leadsto> y2\<close>
      thus ?thesis
        sorry
  qed
next
  case (step y1 z1)

  show ?case
    using step.prems step.IH step.hyps
  proof (induction rule: vm_induct)
    case (base x2)

    have \<open>x2 = y1 \<or> C \<turnstile> x2 \<leadsto> y1\<close>
      using vm_step_trans base.prems(2) base.hyps
      by blast

    thus ?case
    proof (rule disjE)
      assume *: \<open>x2 = y1\<close>
      hence \<open>C \<turnstile> s \<leadsto> z1\<close>
        using step.hyps vm_lift vm_trans
        by blast
      thus ?thesis
        using base.prems base.hyps
        unfolding *
        (* by (rule vm_deterministic) *)
        sorry
    next
      assume \<open>C \<turnstile> x2 \<leadsto> y1\<close>
      thus ?thesis
        using base.prems base.hyps
        sorry
    qed

  next
    case (step y2 z2)

    have \<open>C \<turnstile> s \<leadsto> z2\<close>
      using step.hyps vm_lift vm_trans
      by blast
    hence Eq1: \<open>y1 = z2\<close>
      using step.prems(1)
      by simp

    have \<open>C \<turnstile> s \<leadsto> y2 \<Longrightarrow> y1 = y2\<close>
    proof -
      assume \<open>C \<turnstile> s \<leadsto> y2\<close>
      thus ?thesis
        using step.prems(2)
        (* by (rule vm_deterministic) *)
        sorry
    qed

    thus ?case
      using step.prems step.hyps step.IH
      unfolding Eq1
      by simp
  qed
qed *)

end
