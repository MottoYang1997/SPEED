import numpy as np


## SPICE Detlist Directive
netlist_str = "\
* SPICE Netlist for Boost Topology\n\
* component node_n node_p value\n\
V1 0 1 5\n\
L1 1 2 10u\n\
S1 2 0 100m 10G\n\
S2 2 3 100m 10G\n\
C1 3 0 10u\n\
R1 3 0 100\n\
.end"


## Component Parameters
R_S1 = 100e-3
R_S2 = 10e9
L1 = 10e-6
C1 = 10e-6
R1 = 100


## SPICE Matrix Assembly
A = np.array([[1,-1,0,0,0,0],[0,1,-1,-1,0,0],[0,0,0,1,-1,-1]]) # Built From KCL
S = np.zeros((6,1)) # Built From Component Voltage-Current Relations: External Excitations
K_I = np.zeros((6,6)) # Built From Component Voltage-Current Relations: Impedance
K_V = np.zeros((6,6)) # Built From Component Voltage-Current Relations: Conductance

### V1
K_V[0,0] = 1
#S[0] = 5 # Input Voltage V1
### L1
K_V[1,1] = 1
#S[1] = -1 * L1 * di_L1/dt
### S1
K_I[2,2] = 1
K_V[2,2] = -1 / R_S1
### S2
K_I[3,3] = 1
K_V[3,3] = -1 / R_S2
### C1
K_I[4,4] = 1
#S[4] = -1 * C1 * dv_C1/dt
### R1
K_I[5,5] = 1
K_V[5,5] = -1 / R1

### Selection Matrix vie->x
#vie = np.zeros((6+6+3, 1)) # 6 Branch Currents, 6 Branch Voltages, 3 Node Voltages
#x = np.zeros((2, 1)) # 2 State Variables from L1 and C1
K_x_vie = np.zeros((2, 6+6+3)) # Select x from vie
K_x_vie[0, 1] = 1 # x[0] = i_L1
K_x_vie[1, 10] = 1 # x[1] = v_C1

### Excitation Decomposition: [S,0,0]^T = S_xdot * xdot + S_u * u
S_xdot = np.zeros((6+6+3,2))
S_xdot[1,0] = -1 * L1 # S[1] = -1 * 10e-6 * di_L1/dt
S_xdot[4,1] = -1 * C1 # S[4] = -1 * 10e-6 * dv_C1/dt
S_u = np.zeros((6+6+3, 1))
S_u[0,0] = 1 # S[0] = 1 * 5

### Circuit Equation Matrix with Number of Unknowns: 6 Branch Currents, 6 Branch Voltages, 3 Node Voltages
L0 = np.hstack((K_I, K_V, np.zeros((6,3)))) # 6x6, 6x6, 6x3
L1 = np.hstack((np.zeros((6,6)), np.eye(6), -np.transpose(A))) # 6x6, 6x6, 6x3
L2 = np.hstack((A, np.zeros((3,6)), np.zeros((3,3)))) # 3x6, 3x6, 3x3
L = np.vstack((L0, L1, L2))


## Build Up System Equations
### Dynamic Equations
L_inv = np.linalg.inv(L)
A_sys = np.linalg.inv(K_x_vie @ L_inv @ S_xdot)
B_sys = A_sys @ K_x_vie @ L_inv @ S_u

### Observation Matrix Assembly
K_y_vie = np.zeros((1, 6+6+3)) # y = K_y_vie
K_y_vie[0, (6-1) + 6] = 1 # y[0] = v_R1
K_y_x_dot = K_y_vie @ L_inv
C_sys = K_y_x_dot @ S_xdot @ A_sys
D_sys = K_y_x_dot @ (S_xdot @ B_sys + S_u)


## TODO: Build Up System Equation From Hand Calculation


## TODO: Compare the Two Derivations

