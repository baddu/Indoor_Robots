import robotTourUtil as rtu


def mtsp_main(number_of_groups):
    G = rtu.nx.Graph()
    rtu.data_parser(G, rtu.matrix_input)
    list_of_nodes = list(G.nodes)
    # node that starts first
    source_node_number = 0
    # initialize dictionary
    distance_dictionary = {}
    number_of_iteration = 100
    number_of_groups = number_of_groups
    # pre-processing
    single_robot_mtsp = rtu.mTSP(list_of_nodes, source_node_number, 1, G)
    single_robot_tour = single_robot_mtsp[1][0]
    # for multiple
    print("mTSP for", number_of_groups, "Robots")
    crossover_optimization = []
    iteration_counter = 0
    while iteration_counter < number_of_iteration:
        print("Iteration Number:", iteration_counter + 1)
        if number_of_groups == 1:
            iteration_counter = number_of_iteration - 1
        mtsp_output = rtu.mTSP(single_robot_tour, source_node_number, number_of_groups, G, crossover_optimization)
        fault_flag, iteration_counter = rtu.fault_optimizer(mtsp_output, iteration_counter)
        if fault_flag:
            continue
        # Append to dictionary
        total_length = mtsp_output[0]
        actual_group_path = mtsp_output[1]
        if total_length not in distance_dictionary:
            distance_dictionary[total_length] = [actual_group_path]
        else:
            distance_dictionary[total_length].append(actual_group_path)
        iteration_counter += 1
    # appending to dictionary
    dic_keys = list(distance_dictionary.keys())
    smallest_tour = min(dic_keys)
    print("Paths:")
    print(distance_dictionary[smallest_tour][0])
    print("Total Length:")
    print(smallest_tour)
    print("Length for each robot:")
    for i in range(number_of_groups):
        group_total_length = rtu.calculate_distance(distance_dictionary[smallest_tour][0][i], G)
        print(group_total_length)
    return [distance_dictionary[smallest_tour], smallest_tour]


if __name__ == '__main__':
    mtsp_main(2)
