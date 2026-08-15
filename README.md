# EV Battery SoC/SoH Estimation

Estimating State of Charge (SoC) and State of Health (SoH) for lithium-ion batteries using NASA's battery degradation dataset.
## Current Progress

- Loaded NASA Li-ion battery cycle-level dataset (battery B0005)
- Plotted capacity fade over charge-discharge cycles
- Plotted State of Health (SoH) degradation over cycles

## SoH Validation

Calculated SoH independently as `capacity / capacity[0]` (ratio to initial 
capacity) and compared it against the dataset's provided `soh` column — 
values matched exactly, confirming the formula and dataset are consistent.

## Coulomb Counting (SoC Estimation)

Implemented Coulomb counting from scratch using raw NASA `.mat` data (not 
available in the simplified CSV) to estimate charge removed during a single 
discharge cycle.

**Method:**
- Extracted `Current_measured` and `Time` arrays from cycle 1's raw discharge data
- Applied the trapezoidal rule to integrate current over time:  
  `charge = Σ (average current between two readings) × (time elapsed)`
- Converted the result from Amp-seconds to Amp-hours

**Result:**
- Calculated capacity: **1.8622 Ahr**
- NASA's recorded capacity for the same cycle: **1.8565 Ahr**
- Error: ~0.3%

This small error is expected — it comes from sensor noise and the trapezoidal 
approximation using discrete sampled data rather than continuous measurement. 
This is also why real BMS systems typically combine Coulomb counting with 
voltage-based correction rather than relying on it alone (drift accumulates 
over many cycles).

## Tech Stack

- Python
- pandas
- matplotlib
- scipy

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

## SoC Estimation

Converted Coulomb counting into a running State of Charge (SoC) estimate 
over the full discharge cycle, using two capacity references:

- **Rated capacity (2.0 Ahr, nameplate spec)** — used as the primary SoC 
  definition.
- **Measured capacity (1.862 Ahr, from Coulomb counting)** — Included for comparison only. Since this
  value is obtained from the same Coulomb-counting integration used for the
  SoC calculation, the estimated SoC naturally approaches 0% at the end of
  the discharge cycle and is therefore not used as an independent validation
  reference.


![SoC Estimation](soc_rated_cycle1.png)

SoC drops from 100% to ~6.9% over the discharge (using rated capacity), 
consistent with the Coulomb counting result from earlier. The curve flattens 
near the end as current drops toward zero at the voltage cutoff.