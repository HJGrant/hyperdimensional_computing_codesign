def get_header(temperature):
    return f"""*first line is always a a comment

.include "7nm_modelcard.pm"
.include "cam_periphery/cam_periphery.sp"
.include "rram_cell.sp"
.include "rram_row.sp"

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
+		tran_length		= 11n
+		tran_step		= 'freq_period / 5000'

* set my voltage supplies
v_supply VDD  0 dc=voltage_supply
v_gnd VSS 0 dc=0.0

* set control voltage sources
v_clk CLK 0 pulse (voltage_low voltage_high 0 rise_fall_time rise_fall_time freq_time_high freq_period)
v_precharge_enable PRECH_EN 0 pulse (voltage_low voltage_high 0 rise_fall_time rise_fall_time freq_time_high freq_period)
"""

def init_array_lines(block_size):
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

    netlist_lines.append("\n*======== Initialise Word Lines ========= \n")
    for i in range(block_size):
        netlist_lines.append(f"v_wl{i} WL{i} 0 dc=0.0\n")

    netlist_lines.append("\n*======== Initialise Bit Line ========= \n")
    netlist_lines.append("v_bl BL 0 dc=0.0\n")

    netlist_lines.append("\n*======== Initialise Match Lines ========= \n")
    for i in range(block_size):
        netlist_lines.append(f".IC ML{i} = 0.0\n")

    netlist_lines.append("\n*======== Initialise Rows ========= \n")
    for i in range(block_size):
        row_string = f"x_row{i} " + " ".join(f"QL{j}" for j in range(block_size))
        row_string += f" ML{i} BL WL{i} VSS VDD rram_row\n"
        netlist_lines.append(row_string)

    netlist_lines.append("\n*======== Initialise SA ========= \n")
    for i in range(block_size):
        netlist_lines.append(f"x_sense_amplifier_{i} ML{i} CLK VDD VSS sa_out{str(i)} CSRSA\n")

    netlist_lines.append("\n*======== Initialise Pre-Charge ========= \n")
    for i in range(block_size):
        netlist_lines.append(f"m_precharge_p{i} ML{i} PRECH_EN VDD VDD pmos_rvt nfin=1\n")

    netlist_lines.append(""" 
    .Variation
        .Local_Variation
            pmos pmos_rvt delvtrand=0.015
            nmos nmos_rvt delvtrand=0.015
        .End_Local_Variation
    .End_Variation

    .tran tran_step tran_length UIC SWEEP monte=1000
    \n
    """)

    
    netlist_lines.append("\n*======== Initialise Measure Commands ========= \n")
    for i in range(block_size):
        for j in range(block_size):
            netlist_lines.append(f".measure delay_{str(i)}_{str(j)} trig V(QL{str(j)}) val='voltage_supply/2' rise=1 targ v(sa_out{str(i)}) val='0.1*voltage_supply' fall={str(j+1)} ")




    return "".join(netlist_lines)



def get_rest(vdd):
    return f"""
* define the parameters of my simulation
.param  voltage_supply 	= {vdd}
+		voltage_high	= voltage_supply
+ 		voltage_low		= 0
+ 		rise_fall_time	= 20p 
+		freq_period		= 1n
+		freq_time_high	= '(freq_period / 2) - rise_fall_time'
+		initial_delay	= 1n
+		tran_length		= 11n
+		tran_step		= 'freq_period / 5000'

* set my voltage supplies
v_supply VDD  0 dc=voltage_supply
v_gnd VSS 0 dc=0.0

* set control voltage sources
v_clk CLK 0 pulse (voltage_low voltage_high 0 rise_fall_time rise_fall_time freq_time_high freq_period)
v_precharge_enable PRECH_EN 0 pulse (voltage_low voltage_high 0 rise_fall_time rise_fall_time freq_time_high freq_period)

*define the query signals 
v_q1 QL1 0 pulse (voltage_low voltage_high initial_delay rise_fall_time rise_fall_time freq_time_high freq_period)
v_q2 QL2 0 pulse (voltage_low voltage_high 'initial_delay + freq_period' rise_fall_time rise_fall_time freq_time_high freq_period)
v_q3 QL3 0 pulse (voltage_low voltage_high 'initial_delay + 2*freq_period' rise_fall_time rise_fall_time freq_time_high freq_period)
v_q4 QL4 0 pulse (voltage_low voltage_high 'initial_delay + 3*freq_period' rise_fall_time rise_fall_time freq_time_high freq_period)
v_q5 QL5 0 pulse (voltage_low voltage_high 'initial_delay + 4*freq_period' rise_fall_time rise_fall_time freq_time_high freq_period)
v_q6 QL6 0 pulse (voltage_low voltage_high 'initial_delay + 5*freq_period' rise_fall_time rise_fall_time freq_time_high freq_period)
v_q7 QL7 0 pulse (voltage_low voltage_high 'initial_delay + 6*freq_period' rise_fall_time rise_fall_time freq_time_high freq_period)
v_q8 QL8 0 pulse (voltage_low voltage_high 'initial_delay + 7*freq_period' rise_fall_time rise_fall_time freq_time_high freq_period)
v_q9 QL9 0 pulse (voltage_low voltage_high 'initial_delay + 8*freq_period' rise_fall_time rise_fall_time freq_time_high freq_period)
v_q10 QL10 0 pulse (voltage_low voltage_high 'initial_delay + 9*freq_period' rise_fall_time rise_fall_time freq_time_high freq_period)

*define the opposite of the query signals
v_qb1 QLB1 0 pulse (voltage_high voltage_low initial_delay rise_fall_time rise_fall_time freq_time_high freq_period)
v_qb2 QLB2 0 pulse (voltage_high voltage_low 'initial_delay + freq_period' rise_fall_time rise_fall_time freq_time_high freq_period)
v_qb3 QLB3 0 pulse (voltage_high voltage_low 'initial_delay + 2*freq_period' rise_fall_time rise_fall_time freq_time_high freq_period)
v_qb4 QLB4 0 pulse (voltage_high voltage_low 'initial_delay + 3*freq_period' rise_fall_time rise_fall_time freq_time_high freq_period)
v_qb5 QLB5 0 pulse (voltage_high voltage_low 'initial_delay + 4*freq_period' rise_fall_time rise_fall_time freq_time_high freq_period)
v_qb6 QLB6 0 pulse (voltage_high voltage_low 'initial_delay + 5*freq_period' rise_fall_time rise_fall_time freq_time_high freq_period)
v_qb7 QLB7 0 pulse (voltage_high voltage_low 'initial_delay + 6*freq_period' rise_fall_time rise_fall_time freq_time_high freq_period)
v_qb8 QLB8 0 pulse (voltage_high voltage_low 'initial_delay + 7*freq_period' rise_fall_time rise_fall_time freq_time_high freq_period)
v_qb9 QLB9 0 pulse (voltage_high voltage_low 'initial_delay + 8*freq_period' rise_fall_time rise_fall_time freq_time_high freq_period)
v_qb10 QLB10 0 pulse (voltage_high voltage_low 'initial_delay + 9*freq_period' rise_fall_time rise_fall_time freq_time_high freq_period)

* Wordlines
v_wl0 WL0 0 dc=0.0
v_wl1 WL1 0 dc=0.0

* Bitline
v_bl BL 0 dc=0.0

* Matchlines initial values
.IC ML0 = 0.0
.IC ML1 = 0.0

*********************************************
* Row 0 instance using rram_row
*********************************************
x_row0 QL1_0 QLB1_0 QL2_0 QLB2_0 QL3_0 QLB3_0 QL4_0 QLB4_0 QL5_0 QLB5_0 QL6_0 QLB6_0 QL7_0 QLB7_0 QL8_0 QLB8_0 QL9_0 QLB9_0 QL10_0 QLB10_0 ML0 BL WL0 VSS VDD rram_row

*********************************************
* Row 1 instance using rram_row
*********************************************
x_row1 QL1_1 QLB1_1 QL2_1 QLB2_1 QL3_1 QLB3_1 QL4_1 QLB4_1 QL5_1 QLB5_1 QL6_1 QLB6_1 QL7_1 QLB7_1 QL8_1 QLB8_1 QL9_1 QLB9_1 QL10_1 QLB10_1 ML1 BL WL1 VSS VDD rram_row

x_sense_amplifier_0 ML0 CLK VDD VSS sa_out CSRSA
x_sense_amplifier_1 ML1 CLK VDD VSS sa_out CSRSA

m_precharge_p0 ML0 PRECH_EN VDD VDD pmos_rvt nfin=1
m_precharge_p1 ML1 PRECH_EN VDD VDD pmos_rvt nfin=1


.measure delay_1 trig V(QL1) val='voltage_supply/2' rise=1 targ v(sa_out) val='0.1*voltage_supply' fall=2
.measure delay_2 trig V(QL2) val='voltage_supply/2' rise=1 targ v(sa_out) val='0.1*voltage_supply' fall=3
.measure delay_3 trig V(QL3) val='voltage_supply/2' rise=1 targ v(sa_out) val='0.1*voltage_supply' fall=4
.measure delay_4 trig V(QL4) val='voltage_supply/2' rise=1 targ v(sa_out) val='0.1*voltage_supply' fall=5
.measure delay_5 trig V(QL5) val='voltage_supply/2' rise=1 targ v(sa_out) val='0.1*voltage_supply' fall=6
.measure delay_6 trig V(QL6) val='voltage_supply/2' rise=1 targ v(sa_out) val='0.1*voltage_supply' fall=7
.measure delay_7 trig V(QL7) val='0.1*voltage_supply' rise=1 targ v(sa_out) val='0.1*voltage_supply' fall=8
.measure delay_8 trig V(QL8) val='0.1*voltage_supply' rise=1 targ v(sa_out) val='0.1*voltage_supply' fall=9
.measure delay_9 trig V(QL9) val='0.1*voltage_supply' rise=1 targ v(sa_out) val='0.1*voltage_supply' fall=10
.measure delay_10 trig V(QL10) val='0.1*voltage_supply' rise=1 targ v(sa_out) val='0.1*voltage_supply' fall=11
.measure energy_total INTEGRAL -V(VDD)*I(VDD) FROM=0 TO=tran_length
.measure tops_per_watt PARAM '10 / (energy_total * 1e12)'

.probe v(*)
.END"""