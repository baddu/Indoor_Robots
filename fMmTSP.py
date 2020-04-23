import robotTourUtil as rtu

G = rtu.nx.Graph()
rtu.data_parser(G, rtu.matrix_input)
number_of_nodes = len(list(G.nodes))
list_of_nodes = list(G.nodes)
# depots and number of robots
depots_node = [0,25]
number_of_robots = [2, 2]
final_tour = rtu.MmTSP(list_of_nodes, depots_node, number_of_robots, G)
if final_tour == "SMG" or final_tour == "ED":
    print("SMG/ED - Skip")
else:
    for i in range(len(final_tour)):
        print("Depot:", depots_node[i])
        print("Path:", final_tour[i][0])
        print("Path Length:", final_tour[i][1])
