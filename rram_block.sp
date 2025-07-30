*first line is always a a comment

.include "7nm_modelcard.pm"
.include "cam_periphery/cam_periphery.sp"
.include "rram_cell.sp"

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

*initiate the word line as 0 such that no value from the bitline is written into the Cell
v_wl WL 0 dc=0.0
v_bl BL 0 dc=0.0

* defining a RRAM cell
*.SUBCKT SRAM_CELL QL QLB ML WL BL BLB VSS VDD num_fin=1
x_cell_1 QL1 QLB1 ML BL WL VSS VDD RRAM_CELL num_fin=1
C_load_1 ML 0 0.1f
x_cell_2 QL2 QLB2 ML BL WL VSS VDD RRAM_CELL num_fin=1
C_load_2 ML 0 0.1f
x_cell_3 QL3 QLB3 ML BL WL VSS VDD RRAM_CELL num_fin=1
C_load_3 ML 0 0.1f
x_cell_4 QL4 QLB4 ML BL WL VSS VDD RRAM_CELL num_fin=1
C_load_4 ML 0 0.1f
x_cell_5 QL5 QLB5 ML BL WL VSS VDD RRAM_CELL num_fin=1
C_load_5 ML 0 0.1f
x_cell_6 QL6 QLB6 ML BL WL VSS VDD RRAM_CELL num_fin=1
C_load_6 ML 0 0.1f
x_cell_7 QL7 QLB7 ML BL WL VSS VDD RRAM_CELL num_fin=1
C_load_7 ML 0 0.1f
x_cell_8 QL8 QLB8 ML BL WL VSS VDD RRAM_CELL num_fin=1
C_load_8 ML 0 0.1f
x_cell_9 QL9 QLB9 ML BL WL VSS VDD RRAM_CELL num_fin=1
C_load_9 ML 0 0.1f
x_cell_10 QL10 QLB10 ML BL WL VSS VDD RRAM_CELL num_fin=1
C_load_10 ML 0 0.1f

.IC ML = 0.0 
.IC BL = 0.0

* define the sense amplifier to amplify the ML
x_sense_amplifier ML CLK VDD VSS sa_out CSRSA

* define the precharge transistor
m_precharge_p ML PRECH_EN VDD VDD pmos_rvt nfin=1

.Variation
    .Local_Variation
        pmos pmos_rvt delvtrand=0.015
        nmos nmos_rvt delvtrand=0.015
    .End_Local_Variation
.End_Variation

.tran tran_step tran_length UIC SWEEP monte=1000


*start with measuring the write delay
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

*.measure energy_total INTEGRAL -V(VDD)*I(VDD) FROM=0 TO=tran_length
*.measure tops_per_watt PARAM '10 / (energy_total * 1e12)'

.measure avg_current_1 INTEG i(v_gnd) FROM='initial_delay' TO='initial_delay + freq_period'
.measure avg_power_1 PARAM='avg_current_1 * voltage_supply / (initial_delay + freq_period - initial_delay)'
.measure TOPS_PER_WATT_1 PARAM='1 / (avg_current_1 * voltage_supply * 1e12)'

.measure avg_current_2 INTEG i(v_gnd) FROM='initial_delay + freq_period*2' TO='initial_delay + freq_period*3'
.measure avg_power_2 PARAM='avg_current_2 * voltage_supply / (initial_delay + freq_period*3 - initial_delay + freq_period*2)'
.measure TOPS_PER_WATT_2 PARAM='1 / (avg_current_2 * voltage_supply * 1e12)'

*.probe v(*)
.END