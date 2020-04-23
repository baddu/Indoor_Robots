import robotTourUtil as rtu

G = rtu.nx.Graph()
rtu.data_parser(G, rtu.matrix_input)
number_of_nodes = len(list(G.nodes))
list_of_nodes = list(G.nodes)
number_of_depots = eval(input("Insert number of depots: "))
number_of_robots = [1, 1, 1, 1, 1]
# sort number of robots
number_of_robots.sort(reverse=True)
valid_iterations = False
while not valid_iterations:
    depot_iterations = eval(input("Insert number of iterations: "))
    # check iteration is valid
    total_permutations = rtu.nCr(number_of_nodes, number_of_depots)
    if depot_iterations <= total_permutations:
        valid_iterations = True
    else:
        print("Total Permutation is:", total_permutations)
        print("Pick a smaller iteration")

# produce optimal
universal_dict = {}
depots_node_test = []
for depot_node in range(depot_iterations):
    print("Depot Iteration Number: ", depot_node + 1)
    unique_depot = False
    while not unique_depot:
        depots_node = []
        i = 0
        while i < number_of_depots != 1:
            random_integer = rtu.random.randint(0, number_of_nodes - 1)
            if random_integer not in depots_node:
                depots_node.append(random_integer)
                i += 1
            else:
                continue
        if number_of_depots == 1:
            random_integer = rtu.random.randint(0, number_of_nodes - 1)
            depots_node.append(random_integer)
        if depots_node not in depots_node_test:
            unique_depot = True
            depots_node_test.append(depots_node)
    mmtsp_output = rtu.MmTSP(list_of_nodes, depots_node, number_of_robots, G, [5, 65])
    if type(mmtsp_output) == str:
        if mmtsp_output == "SMG":
            print("SMG error - Pick Different Depots")
        elif mmtsp_output == "ED":
            print("ED error - Pick Different Depots")
        elif mmtsp_output == "DGS":
            print("DGS error - Pick Different Depots")
        elif mmtsp_output == "NS":
            print("NS error - No Solutions")
        continue
    distance_key = 0
    for i in range(len(mmtsp_output)):
        distance_key += mmtsp_output[i][1]
    if distance_key not in universal_dict:
        universal_dict[distance_key] = [[depots_node, mmtsp_output]]
    else:
        universal_dict[distance_key].append([depots_node, mmtsp_output])
# pick smallest distance
final_tour = []
dic_keys = list(universal_dict.keys())
smallest_tour = min(dic_keys)
print("Smallest Distance is:", smallest_tour)
print("Depot Assigned:", universal_dict[smallest_tour][0][0])
print("Path of Each Robot:", universal_dict[smallest_tour][0][1])
