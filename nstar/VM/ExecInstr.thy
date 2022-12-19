theory ExecInstr
  imports
    Main
    VM.VMState
begin

primrec exec_instr :: \<open>[ pc, instr, exec_reg_set, labels ] \<Rightarrow> state\<close>
where \<open>exec_instr pc Halt \<chi> \<Xi> = (None, \<chi>, \<Xi>)\<close>
    | \<open>exec_instr pc (Move v r) \<chi> \<Xi> = (Some (Suc pc), \<chi>[r ≔ v], \<Xi>)\<close>
    | \<open>exec_instr _ (Jump lbl) \<chi> \<Xi> = (\<Xi> lbl, \<chi>, \<Xi>)\<close>

end
