#!/usr/bin/env python
import sys
if len(sys.argv) < 2:
    print("Usage: ./process_data.py file_name_preprocessed file_name_processed")
    print("Output: file_name_processed")
    exit(1)

file_name = sys.argv[1]
output_file_name = sys.argv[2]
num_core = int(sys.argv[3])
try:
    with open(file_name, "r") as data:
        lines = data.readlines()
        lines = [line.strip() for line in lines]
except Exception as e:
    print(f"Exception {e}")
    exit(1)

sim_inst_count = int(lines[0])

cpu = []

for i in range(num_core):
    global_mpki = float(lines[1])
    ipc = float(lines[2])

    # row: total access, hit, miss, mpki, avg miss cycle
    rows, cols= (4,5)
    cache_data = [[0 for i in range(cols)] for j in range(rows)]


    for idx, line in enumerate(lines[(2*i):]):
        if not line:
            continue

        # print(idx, line)
        if (idx % 2) == 0:
            cache_data[idx//2][0:3] = map(lambda x: int(x) , line.split(' '))
            cache_data[idx//2][3] = (cache_data[idx//2][2] * 1000)/sim_inst_count
        else:
            cache_data[idx//2][4]= float(line)

    # print(global_mpki)
    # print(ipc)
    # print(cache_data)
    cpu.append((global_mpki, ipc, cache_data))

print(sim_inst_count)       
print(cpu)
exit()

with open(output_file_name, "w") as outfile:
    outfile.write(str(sim_inst_count))
    outfile.write("\n")
    outfile.write(str(global_mpki))
    outfile.write("\n")
    outfile.write(str(ipc))
    outfile.write("\n")
    for data in cache_data:
        for val in data:
            outfile.write(str(val) + " ")
        outfile.write("\n")


cache_total, cache_hit, cache_miss , cache_mpki = "{cache}_total", "{cache}_hit", "{cache}_miss" , "{cache}_mpki" 
cache_avg_miss_cycles = "{cache}_avg_miss_cycles"
cache_names = ["L1D", "L1I", "L2C", "LLC"]

# for cache_name in cache_names:
#    print(cache_total.format(cache=cache_name), cache_hit.format(cache=cache_name), cache_miss.format(cache=cache_name), cache_avg_miss_cycles.format(cache=cache_name))
