* A=input; Y=output
.SUBCKT INV_x1 A VDD VSS Y PU=3 PD=3
M_0 Y A VSS VSS nmos_rvt nfin=PD
M_1 Y A VDD VDD pmos_rvt nfin=PU
ca A VSS 0.39913f
.ENDS

.SUBCKT BUF_x1 A VDD VSS Y strength=3
x_inv1 A VDD VSS AN INV_x1 PU=strength PD=strength
x_inv2 AN VDD VSS Y INV_x1 PU=strength PD=strength
.ENDS

.subckt CSRSA in clk vdd vss sa_out

M_pre sn clk VDD VDD pmos_rvt
m_npre sn out in VSS nmos_rvt

M_n1  out  in  vss  vss nmos_rvt
M_p1  out  in  vdd  vdd pmos_rvt
M_n21 out  in  net1 vss nmos_rvt
M_n22 net1 clk vss  vss nmos_rvt
M_p21 out  in  net2 vdd pmos_rvt
M_p22 net2 clk vdd  vdd pmos_rvt

x_buf sn VDD VSS sa_out BUF_x1
.ends CSRSA