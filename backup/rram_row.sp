* rram_row.sp — Subcircuit for one RRAM row (10 RRAM cells wide)
* Node order: QL1 QLB1 QL2 QLB2 ... QL10 QLB10 ML BL WL VSS VDD
.SUBCKT rram_row QL1 QLB1 QL2 QLB2 QL3 QLB3 QL4 QLB4 QL5 QLB5 \
                  QL6 QLB6 QL7 QLB7 QL8 QLB8 QL9 QLB9 QL10 QLB10 \
                  ML BL WL VSS VDD

X1  QL1  QLB1  ML  BL  WL  VSS VDD RRAM_CELL num_fin=1
C1  ML  0  0.1f

X2  QL2  QLB2  ML  BL  WL  VSS VDD RRAM_CELL num_fin=1
C2  ML  0  0.1f

X3  QL3  QLB3  ML  BL  WL  VSS VDD RRAM_CELL num_fin=1
C3  ML  0  0.1f

X4  QL4  QLB4  ML  BL  WL  VSS VDD RRAM_CELL num_fin=1
C4  ML  0  0.1f

X5  QL5  QLB5  ML  BL  WL  VSS VDD RRAM_CELL num_fin=1
C5  ML  0  0.1f

X6  QL6  QLB6  ML  BL  WL  VSS VDD RRAM_CELL num_fin=1
C6  ML  0  0.1f

X7  QL7  QLB7  ML  BL  WL  VSS VDD RRAM_CELL num_fin=1
C7  ML  0  0.1f

X8  QL8  QLB8  ML  BL  WL  VSS VDD RRAM_CELL num_fin=1
C8  ML  0  0.1f

X9  QL9  QLB9  ML  BL  WL  VSS VDD RRAM_CELL num_fin=1
C9  ML  0  0.1f

X10 QL10 QLB10 ML  BL  WL  VSS VDD RRAM_CELL num_fin=1
C10 ML  0  0.1f

.ENDS rram_row