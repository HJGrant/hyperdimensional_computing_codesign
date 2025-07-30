.include "7nm_modelcard.pm"
.include "cam_periphery/cam_periphery.sp"
.include "rram_cell.sp"
.include "rram_row.sp"

.option post ingold=2 lis_new 

* define the temperature 
.option measform=3
.option run_lvl=3
.TEMP 27

* define the parameters of my simulation
.param  voltage_supply 	= 0.7
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
x_row0 QL1 QLB1 QL2 QLB2 QL3 QLB3 QL4 QLB4 QL5 QLB5 QL6 QLB6 QL7 QLB7 QL8 QLB8 QL9 QLB9 QL10 QLB10 ML0 BL WL0 VSS VDD rram_row

*********************************************
* Row 1 instance using rram_row
*********************************************
x_row1 QL1 QLB1 QL2 QLB2 QL3 QLB3 QL4 QLB4 QL5 QLB5 QL6 QLB6 QL7 QLB7 QL8 QLB8 QL9 QLB9 QL10 QLB10 ML1 BL WL1 VSS VDD rram_row

x_sense_amplifier_0 ML0 CLK VDD VSS sa_out0 CSRSA
x_sense_amplifier_1 ML1 CLK VDD VSS sa_out1 CSRSA

m_precharge_p0 ML0 PRECH_EN VDD VDD pmos_rvt nfin=1
m_precharge_p1 ML1 PRECH_EN VDD VDD pmos_rvt nfin=1


.measure delay_0_1 trig V(QL1) val='voltage_supply/2' rise=1 targ v(sa_out0) val='0.1*voltage_supply' fall=2
.measure delay_0_2 trig V(QL2) val='voltage_supply/2' rise=1 targ v(sa_out0) val='0.1*voltage_supply' fall=3
.measure delay_0_3 trig V(QL3) val='voltage_supply/2' rise=1 targ v(sa_out0) val='0.1*voltage_supply' fall=4
.measure delay_0_4 trig V(QL4) val='voltage_supply/2' rise=1 targ v(sa_out0) val='0.1*voltage_supply' fall=5
.measure delay_0_5 trig V(QL5) val='voltage_supply/2' rise=1 targ v(sa_out0) val='0.1*voltage_supply' fall=6
.measure delay_0_6 trig V(QL6) val='voltage_supply/2' rise=1 targ v(sa_out0) val='0.1*voltage_supply' fall=7
.measure delay_0_7 trig V(QL7) val='0.1*voltage_supply' rise=1 targ v(sa_out0) val='0.1*voltage_supply' fall=8
.measure delay_0_8 trig V(QL8) val='0.1*voltage_supply' rise=1 targ v(sa_out0) val='0.1*voltage_supply' fall=9
.measure delay_0_9 trig V(QL9) val='0.1*voltage_supply' rise=1 targ v(sa_out0) val='0.1*voltage_supply' fall=10
.measure delay_0_10 trig V(QL10) val='0.1*voltage_supply' rise=1 targ v(sa_out0) val='0.1*voltage_supply' fall=11

.measure delay_1_1 trig V(QL1) val='voltage_supply/2' rise=1 targ v(sa_out1) val='0.1*voltage_supply' fall=2
.measure delay_1_2 trig V(QL2) val='voltage_supply/2' rise=1 targ v(sa_out1) val='0.1*voltage_supply' fall=3
.measure delay_1_3 trig V(QL3) val='voltage_supply/2' rise=1 targ v(sa_out1) val='0.1*voltage_supply' fall=4
.measure delay_1_4 trig V(QL4) val='voltage_supply/2' rise=1 targ v(sa_out1) val='0.1*voltage_supply' fall=5
.measure delay_1_5 trig V(QL5) val='voltage_supply/2' rise=1 targ v(sa_out1) val='0.1*voltage_supply' fall=6
.measure delay_1_6 trig V(QL6) val='voltage_supply/2' rise=1 targ v(sa_out1) val='0.1*voltage_supply' fall=7
.measure delay_1_7 trig V(QL7) val='0.1*voltage_supply' rise=1 targ v(sa_out1) val='0.1*voltage_supply' fall=8
.measure delay_1_8 trig V(QL8) val='0.1*voltage_supply' rise=1 targ v(sa_out1) val='0.1*voltage_supply' fall=9
.measure delay_1_9 trig V(QL9) val='0.1*voltage_supply' rise=1 targ v(sa_out1) val='0.1*voltage_supply' fall=10
.measure delay_1_10 trig V(QL10) val='0.1*voltage_supply' rise=1 targ v(sa_out1) val='0.1*voltage_supply' fall=11

.measure avg_delay_1 param='(delay_0_1 + delay_1_1)/2'
.measure avg_delay_2 param='(delay_0_2 + delay_1_2)/2'
.measure avg_delay_3 param='(delay_0_3 + delay_1_3)/2'
.measure avg_delay_4 param='(delay_0_4 + delay_1_4)/2'
.measure avg_delay_5 param='(delay_0_5 + delay_1_5)/2'
.measure avg_delay_6 param='(delay_0_6 + delay_1_6)/2'
.measure avg_delay_7 param='(delay_0_7 + delay_1_7)/2'
.measure avg_delay_8 param='(delay_0_8 + delay_1_8)/2'
.measure avg_delay_9 param='(delay_0_9 + delay_1_9)/2'
.measure avg_delay_10 param='(delay_0_10 + delay_1_10)/2'

.measure avg_current INTEG i(v_gnd) FROM='initial_delay' TO='tran_length'
.measure TOPS_PER_WATT PARAM='20 / (avg_current * voltage_supply * 1e12)'
.measure avg_power PARAM='avg_current * voltage_supply / (tran_length - initial_delay)'

*.probe v(*)
.END