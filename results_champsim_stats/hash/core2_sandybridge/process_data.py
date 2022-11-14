#!/usr/bin/env python
import sys

def process_file(file_name, num_core):
    try:
        with open(file_name, "r") as data:
            lines = data.readlines()
            lines = [line.strip() for line in lines]
    except Exception as e:
        print(f"Exception {e}")
        exit(1)

    sim_inst_count = int(lines[0])

    cpu = []

    for j in range(1,7*num_core + 1,7):
        print(lines[j])
        global_mpki = float(lines[j])
        ipc = float(lines[j + 1])

        rows, cols = (5,4)
        cache_data = [[0 for p in range(cols)] for q in range(rows)]


        for k in range(5):
            line = lines[j+2+k]
            if not line:
                continue
            cache_data[k][0:3] = map(lambda x: int(x) , line.split(' '))
            cache_data[k][3] = (cache_data[k][2] * 1000)/sim_inst_count

        cpu.append((global_mpki, ipc, cache_data))

    return sim_inst_count, cpu

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./process_data.py file_name_preprocessed num_cores")
        print("Output: sim_inst_count, per cpu data")
        exit(1)

    file_name = sys.argv[1]
    # output_file_name = sys.argv[2]
    num_core = int(sys.argv[2])
    sim_inst_count, cpu = process_file(file_name, num_core)
    print(sim_inst_count, cpu)
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
