// SRAM cell subcircuit
* NAME N_DRAIN N_GATE N_SOURCE N_BULK TransistorType [instance parameters]
.SUBCKT SRAM_CELL QL QLB ML WL VSS VDD num_fin=1

*left side of the cell
m_left_top_n internal_ql_cb CB ML ML nmos_rvt nfin=num_fin
m_left_bottom_n internal_ql_cb QL VSS VSS nmos_rvt nfin=num_fin

*right side of the cell
m_right_top_n internal_qlb_c C ML ML nmos_rvt nfin=num_fin
m_right_bottom_n internal_qlb_c QLB VSS VSS nmos_rvt nfin=num_fin

*define the inverters 
x_top_inv CB VDD VSS C INV_x1
x_bottom_inv C VDD VSS CB INV_x1 

*define the access transistors
m_pg_l CB WL BLB BLB nmos_rvt nfin=num_fin
m_pg_r C WL BL BL nmos_rvt nfin=num_fin

*define the load capacitors
C_c_cap C 0 0.03f
C_cb_cap CB 0 0.03f

.ENDS