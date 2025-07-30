// SRAM cell subcircuit
* NAME N_DRAIN N_GATE N_SOURCE N_BULK TransistorType [instance parameters]
.SUBCKT RRAM_CELL QL QLB ML BL WL VSS VDD ron=10000 roff=100000 num_fin=1

*left side of the cell
R_RRAM_L QL internal_node ron

*right side of the cell
R_RRAM_R internal_node QLB roff

*define the access transistor
m_prg_tran internal_node WL BL nmos_rvt nfin=num_fin

* define the discharge transistor
m_pull_down_trans ML internal_node VSS VSS nmos_rvt nfin=num_fin

*define the load capacitors
C_c_cap internal_node 0 0.03f

.ENDS