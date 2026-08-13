# EV Battery SoC/SoH Estimation

Estimating State of Charge (SoC) and State of Health (SoH) for lithium-ion batteries using NASA's battery degradation dataset.
## Current Progress

- Loaded NASA Li-ion battery cycle-level dataset (battery B0005)
- Plotted capacity fade over charge-discharge cycles
- Plotted State of Health (SoH) degradation over cycles

## Tech Stack

- Python
- pandas
- matplotlib

## Results


### Voltage per Cycle
![Voltage](b0005_voltage.png)

Voltage peaks around 3.6V then trends down to ~3.46V as the battery ages — 
rising internal resistance causes voltage droop, making this a secondary 
signal for estimating SoH alongside capacity.

### Temperature per Cycle
![Temperature](b0005_temperature.png)

Temperature is noisy with a few sharp spikes. These may correlate with 
capacity recovery bumps seen in the fade curve — a known effect where heat 
temporarily restores some usable capacity in Li-ion cells.

### Capacity Fade
![Capacity Fade](b0005_capacity.png)
Capacity drops from ~1.86 Ahr to ~1.33 Ahr over 168 cycles, reaching the 
70% End-of-Life threshold commonly used in industry.

### State of Health Degradation
![SoH Degradation](SoH_b00005.png)
SoH is calculated as capacity relative to initial capacity, so it mirrors 
the capacity fade curve exactly.
