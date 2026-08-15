import scipy.io
mat = scipy.io.loadmat("B0005.mat")
cycles = mat["B0005"][0, 0]["cycle"][0]
discharge_cycle = [c for c in cycles if c["type"][0] == "discharge"]
one_discharge = discharge_cycle[0]
current = one_discharge["data"]["Current_measured"][0, 0][0]
time = one_discharge["data"]["Time"][0, 0][0]
print(current.shape)
print(time.shape)
#calculating with rated capacity reference
rated_capacity = 2.0
soc_rated = [100.0]
for i in range(1, len(current)):
    dt = time[i]-time[i-1]
    avg_current = (current[i] + current[i-1])/2
    charge_step = abs(avg_current) * dt /3600
    soc_drop = (charge_step/rated_capacity) * 100
    new_soc = soc_rated[-1] - soc_drop
    soc_rated.append(new_soc)

print("SoC at the end is : ", soc_rated[-1], "%")

#calculating with measured capacity
measured_cap = 1.8621974749807595
soc_measured = [100.0]
for i in range(1, len(current)):
    dt = time[i]-time[i-1]
    avg_current = (current[i] + current[i - 1]) / 2
    charge_step = abs(avg_current) * dt / 3600
    soc_drop = (charge_step / measured_cap) * 100
    new_soc = soc_measured[-1] - soc_drop
    soc_measured.append(new_soc)

print("SoC at the end is(measured capacity) : ", soc_measured[-1], "%")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.figure()
plt.plot(time, soc_rated)
plt.xlabel("Time (s)")
plt.ylabel("SoC (%)")
plt.title("B0005 - SoC Estimation (Rated Capacity) - Cycle 1 Discharge")
plt.grid(True)
plt.savefig("soc_rated_cycle1.png")
print("Saved SoC plot!")

plt.figure()
plt.plot(time, current)
plt.xlabel("Time (s)")
plt.ylabel("Current (A)")
plt.title("B0005 - Current During Discharge - Cycle 1")
plt.grid(True)
plt.savefig("current_cycle1.png")
print("Saved current plot!")