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

### Current During Discharge

![Current During Discharge](current_cycle1.png)

Current stays roughly constant around -2.0 A for most of the discharge 
(after a brief initial ramp-up), which explains why the SoC curve above is 
nearly linear — a steady current means SoC drops by a roughly fixed amount 
at each time step. Real-world usage with variable current draw would produce a non-linear SoC trajectory instead.

## Coulomb Counting Across All Cycles

Extended Coulomb counting from a single cycle to all 168 discharge cycles, 
generating an independent capacity estimate for the battery's entire life 
and saving results to `my_coulomb_counting_results.csv`.

![Coulomb Counting vs NASA, All Cycles](coulomb_counting_all_cycles.png)

My calculated capacity tracks NASA's recorded capacity closely across all 
168 cycles, with a small, consistent offset (my values run slightly higher 
throughout) rather than random error — suggesting a small systematic bias 
in the trapezoidal integration method rather than accumulating drift. This 
confirms Coulomb counting stays reliable across the battery's full life, 
not just for a single cycle.

## OCV Approximation (Voltage vs SoC)

Plotted voltage against SoC (using rated capacity) for cycle 1's discharge, 
since Coulomb counting alone drifts over time and voltage-based SoC lookup 
is the standard real-world correction method.

**Important caveat:** this is not true Open Circuit Voltage, since the 
battery is under a constant ~2A load throughout discharge, never at rest. 
The measured voltage is lower than true OCV by an amount proportional to 
internal resistance (`V_measured = V_OCV - I × R_internal`). This is best 
understood as a "quasi-OCV" curve — useful for showing the characteristic 
shape, but not a substitute for true rest-voltage measurements.

![Voltage vs SoC](VTG_VS_SoC_cycle1.png)

The curve shows the classic Li-ion S-shape: steep near full charge (90-100% 
SoC) and near empty (below ~15% SoC), with a flat middle region (20-90% SoC) 
where voltage is a poor indicator of SoC on its own — this is why Coulomb 
counting and voltage-based methods are complementary rather than 
interchangeable.

**Artifact near cutoff:** a small voltage recovery near SoC ~7% was verified 
against the raw current data — current drops to near-zero in the final 
readings (test rig detecting cutoff), which reduces the internal-resistance 
voltage drop and causes voltage to rise slightly even as SoC stays roughly 
constant. This confirms the dip is a real physical effect, not sensor noise.