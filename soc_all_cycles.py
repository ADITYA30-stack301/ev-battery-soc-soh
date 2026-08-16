import scipy.io
mat = scipy.io.loadmat("B0005.mat")
cycles = mat["B0005"][0, 0]["cycle"][0]
discharge_cycle = [c for c in cycles if c["type"][0] == "discharge"]

my_capacities = []
nasa_capacities = []
cycle_no = []

for idx , dc in enumerate(discharge_cycle) :
    current = dc["data"]["Current_measured"][0,0][0]
    time = dc["data"]["Time"][0, 0][0]

    charge_removed = 0
    for i in range(1, len(current)):
        dt = time[i] - time[i - 1]
        avg_current = (current[i] + current[i - 1]) / 2
        charge_removed += abs(avg_current) * dt

    my_capacity = charge_removed/3600;
    nasa_capacity = dc["data"]["Capacity"][0, 0][0][0]

    my_capacities.append(my_capacity)
    nasa_capacities.append(nasa_capacity)
    cycle_no.append(idx +1)

print("Done. Processed", len(my_capacities), "cycles")
print(my_capacities[:5])
print(nasa_capacities[:5])

import pandas as pd
results = pd.DataFrame({
    "cycle": cycle_no,
    "my_capacity": my_capacities,
    "nasa_capacity": nasa_capacities
})

results.to_csv("my_coulomb_counting_results.csv", index=False)
print("Saved results CSV!")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

results_pd = pd.read_csv("my_coulomb_counting_results.csv")


plt.figure()
plt.plot(results_pd["cycle"], results_pd["my_capacity"], label="My Coulomb Counting")
plt.plot(results_pd["cycle"], results_pd["nasa_capacity"], label="NASA Recorded")
plt.xlabel("Cycle")
plt.ylabel("Capacity (Ahr)")
plt.title("B0005 - Coulomb Counting vs NASA Capacity, All Discharge Cycles(168)")
plt.legend()
plt.grid(True)
plt.savefig("coulomb_counting_all_cycles.png")
print("Saved comparison plot!")

error = results_pd["my_capacity"] - results_pd["nasa_capacity"]
percent_error = (error/results_pd["nasa_capacity"])*100

mean_abs_error = error.abs().mean()
mean_percent_error = percent_error.abs().mean()
max_percent_error = percent_error.abs().max()

import numpy as np

rmse = np.sqrt((error ** 2).mean())

print("Mean Absolute Error (Ahr):", mean_abs_error)
print("Root Mean Square Error (Ahr):", rmse)
print("Mean Percent Error (%):", mean_percent_error)
print("Max Percent Error (%):", max_percent_error)


