import robotTourUtil as rtu

G = rtu.nx.Graph()
rtu.data_parser(G, rtu.matrix_input)
number_of_nodes = len(list(G.nodes))
list_of_nodes = list(G.nodes)

###################  USER INUPUT ##############################################

# input the depot nodes
depots_node = [0,10,25]

#input the number of robots in each depot
number_of_robots = [1, 1,1]

###############################################################################

final_tour = rtu.MmTSP(list_of_nodes, depots_node, number_of_robots, G)
if final_tour == "SMG" or final_tour == "ED":
    #print("testing")
    print("SMG/ED - Skip")
else:
    total_path_length = 0
    for i in range(len(final_tour)):
        print("\nWorking on Depot:", depots_node[i])
        print("Path for each of the robots in this depot is:", final_tour[i][0])
        total_path_length = total_path_length+ final_tour[i][1]
        print("Subtotal path length for robots in this depot is:", final_tour[i][1])
        print("\nTotal path length for all robots is:", total_path_length)
