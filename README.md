# SPEED
Switched Power Electronics Evaluator and Designer

## What is SPEED
An online switch power supply evaluator/designer with the following capabilities:
+ Input: Schematic (with or without GUI) and SPICE Directives
+ Output: DC Operation Point for each component and Small Signal Frequency Response
    + Possible Simulation Techniques to be Adapted
        1. State Averaging
        1. State Averaging with Expanded Bandwidth
        1. Harmonic Balance With Galerkin's Method
    + Probable Front End Tech Stacks
        1. React
        1. Web Worker

## TODOs (Intermediate Steps):
### Algorithm Verification
+ Lossy Buck CCM Model
+ Lossy Boost CCM Model
+ Lossy Forward CCM Model
+ Lossy Flyback CCM Model
### Further Works on Coupled Inductor Device Model
### Further Works on Transformer Device Model
### Duty Cycle Calculation with DCM
### SPICE Parsing
### Matrix Assembly
### Website GUI Design