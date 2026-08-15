import scipy.io
mat = scipy.io.loadmat("B0005.mat")
print(mat.keys())
print(mat["B0005"])
b5_struct = mat["B0005"][0, 0]
cycles =b5_struct["cycle"][0]
print(cycles.shape)
for i in range(5):
    print(i, cycles[i]["type"][0])
discharge_cycle = [c for c in cycles if c["type"][0]=="discharge"]
print(len(discharge_cycle))
one_discharge = discharge_cycle[0]
print(one_discharge["data"].dtype.names)
current = one_discharge["data"]["Current_measured"][0, 0][0]
time = one_discharge["data"]["Time"][0, 0][0]
print(current.shape)
print(time.shape)
print(current[:10])
print(time[:10])


charge_removed = 0
for i in range(1, len(current)):
    dt = time[i] - time[i-1]
    avg_current = (current[i]+ current[i-1])/2
    charge_removed += abs(avg_current) * dt

print("Total charge removed (Amp-seconds):", charge_removed)
print("Total charge removed (Amp-hours):", charge_removed / 3600)

nasa_capacity = one_discharge["data"]["Capacity"][0, 0][0][0]
print("NASA's recorded capacity for this cycle:", nasa_capacity)