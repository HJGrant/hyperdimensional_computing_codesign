import numpy as np 

def get_header(temperature):
    return f"""*first line is always a a comment

.include "7nm_modelcard.pm"
.include "cam_periphery/cam_periphery.sp"
.include "rram_cell.sp"

.option post ingold=2 lis_new 

* define the temperature 
.option measform=3
.option run_lvl=3
.TEMP {temperature}
"""

def initial_setup(vdd):
    return f"""
* define the parameters of my simulation
.param  voltage_supply 	= {vdd}
+		voltage_high	= voltage_supply
+ 		voltage_low		= 0
+ 		rise_fall_time	= 20p 
+		freq_period		= 1n
+		freq_time_high	= '(freq_period / 2) - rise_fall_time'
+		initial_delay	= 1n
+		tran_length		= 20n
+		tran_step		= 'freq_period / 5000'

* set my voltage supplies
v_supply VDD  0 dc=voltage_supply
v_gnd VSS 0 dc=0.0

* set control voltage sources
v_clk CLK 0 pulse (voltage_low voltage_high 0 rise_fall_time rise_fall_time freq_time_high freq_period)
v_precharge_enable PRECH_EN 0 pulse (voltage_low voltage_high 0 rise_fall_time rise_fall_time freq_time_high freq_period)
"""

def init_array_lines(block_size, vec_dim):
    netlist_lines = []

    netlist_lines.append("*======== Initialise QLs ========= \n")
    netlist_lines.append('v_q0 QL0 0 pulse (voltage_low voltage_high initial_delay rise_fall_time rise_fall_time freq_time_high freq_period)\n')
    for i in range(1, block_size):
        netlist_lines.append(
            f"v_q{i} QL{i} 0 pulse (voltage_low voltage_high 'initial_delay + {i}*freq_period' rise_fall_time rise_fall_time freq_time_high freq_period)\n"
        )

    netlist_lines.append("\n*======== Initialise QLBs ========= \n")
    netlist_lines.append("v_qb0 QLB0 0 pulse (voltage_high voltage_low initial_delay rise_fall_time rise_fall_time freq_time_high freq_period)\n")
    for i in range(1, block_size):
        netlist_lines.append(
            f"v_qb{i} QLB{i} 0 pulse (voltage_high voltage_low 'initial_delay + {i}*freq_period' rise_fall_time rise_fall_time freq_time_high freq_period)\n"
        )

    netlist_lines.append(f"v_wl WL 0 dc=0.0\n")
    netlist_lines.append("v_bl BL 0 dc=0.0\n")

    netlist_lines.append("\n*======== Initialise Cells ========= \n")
    for i in range(block_size):
        netlist_lines.append(f"x_cell_{str(i)} QL{str(i)} QLB{str(i)} ML BL WL VSS VDD RRAM_CELL num_fin=1\n")
        netlist_lines.append(f"C_load_{str(i)} ML 0 0.1f\n")


    netlist_lines.append(f"\n.IC ML = 0.0\n")
    netlist_lines.append(f".IC BL = 0.0\n")


    netlist_lines.append(f"\nx_sense_amplifier ML CLK VDD VSS sa_out CSRSA\n")
    netlist_lines.append(f"m_precharge_p ML PRECH_EN VDD VDD pmos_rvt nfin=1\n")

    netlist_lines.append("""\n 
.Variation
    .Local_Variation
        pmos pmos_rvt delvtrand=0.015
        nmos nmos_rvt delvtrand=0.015
    .End_Local_Variation
.End_Variation

.tran tran_step tran_length UIC SWEEP monte=1000
    \n
    """)

    netlist_lines.append("\n*======== Initialise Delay Measurement ========= \n")
    for i in range(block_size):
        netlist_lines.append(f".measure delay_{str(i)} trig V(QL{str(i)}) val='voltage_supply/2' rise=1 targ v(sa_out) val='0.1*voltage_supply' fall={str(i+2)}\n")
    
    netlist_lines.append("\n*======== Initialise Enegry Measurement ========= \n")
    netlist_lines.append(f"\n.measure avg_current INTEG i(v_gnd) FROM='initial_delay' TO='initial_delay + freq_period'\n")
    netlist_lines.append(f".measure avg_power PARAM='avg_current * voltage_supply / (freq_period)'\n")
    netlist_lines.append(f".measure avg_power_vec PARAM='avg_power * {np.floor(vec_dim/block_size)}'\n")

    netlist_lines.append("\n.END")
    
    return "".join(netlist_lines)