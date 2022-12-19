theory Registers
  imports Main
begin

datatype reg =
  R0
| R1
| R2
| R3
| R4
| R5

lemma UNIV_reg: \<open>UNIV = {R0, R1, R2, R3, R4, R5}\<close>
  by (auto intro: reg.exhaust)

instantiation reg :: enum
begin
  definition
    \<open>enum_reg \<equiv> [R0, R1, R2, R3, R4, R5]\<close>

  definition
    \<open>enum_all_reg P \<equiv> P R0 \<and> P R1 \<and> P R2 \<and> P R3 \<and> P R4 \<and> P R5\<close>

  definition
    \<open>enum_ex_reg P \<equiv> P R0 \<or> P R1 \<or> P R2 \<or> P R3 \<or> P R4 \<or> P R5\<close>

  instance by standard
    (simp_all add: enum_reg_def enum_all_reg_def enum_ex_reg_def UNIV_reg)
end

type_synonym 'a reg_set = \<open>reg \<rightharpoonup> 'a\<close>

abbreviation empty :: \<open>'a reg_set\<close> (\<open>\<emptyset>\<close>)
where \<open>\<emptyset> \<equiv> \<lambda>r. None\<close>

fun extend :: \<open>'a reg_set \<Rightarrow> reg \<Rightarrow> 'a \<Rightarrow> 'a reg_set\<close> (\<open>_ [ _ ≔ _]\<close> [89, 92, 92] 90)
where \<open>extend f r x = f(r \<mapsto> x)\<close> (* (\<lambda>r2. if r1 = r2 then Some x else f r2) *)

fun access :: \<open>'a reg_set \<Rightarrow> reg \<Rightarrow> 'a option\<close> (\<open>_ !@ _\<close> [71, 71] 70)
where \<open>access f r = f r\<close>

(*****************************************************************)

lemma extend_access:
  fixes r :: reg
    and x :: 'a
    and f :: \<open>'a reg_set\<close>
  shows \<open>(f[r ≔ x] !@ r) = Some x\<close>
  by simp

lemma extend_access_other:
  fixes r1 r2 :: reg
    and x :: 'a
    and f :: \<open>'a reg_set\<close>
  assumes \<open>r1 \<noteq> r2\<close>
  shows \<open>(f[r1 ≔ x] !@ r2) = (f !@ r2)\<close>
  using assms
  by simp

lemma empty_is_empty:
  fixes r :: reg
  shows \<open>\<emptyset> !@ r = None\<close>
  by simp

end
