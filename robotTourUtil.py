import tsp
import networkx as nx
import copy
import random
import math
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

###################  USER INUPUT ##############################################
# undirected graph network elements
# [node1, node2, edge_length]
matrix_input = [[0, 1, 9.8], [0, 3, 2],
                [1, 2, 3.5], [1, 7, 2.7],
                [2, 12, 5.5],
                [3, 4, 3], [3, 8, 2],
                [4, 5, 2.2], [4, 10, 3.7],
                [5, 6, 3.6], [5, 14, 8.0],
                [6, 7, 0.9], [6, 15, 8.0],
                [8, 9, 1.7],
                [9, 10, 2.1],
                [10, 13, 4.3],
                [11, 12, 2.2], [11, 16, 4.5],
                [13, 14, 2.2], [13, 18, 3.8],
                [14, 15, 3.6], [14, 24, 9.1],
                [15, 16, 2.2],
                [16, 21, 4.1],
                [17, 18, 1.1], [17, 20, 0.9],
                [19, 20, 0.7], [19, 23, 4.4],
                [21, 22, 2.2], [21, 25, 5.0],
                [22, 26, 5.0],
                [23, 24, 4.0],
                [24, 25, 5.8],
                [25, 26, 2.2]
                ]
###############################################################################


def data_parser(networkx_graph, matrix):
    for i in range(len(matrix)):
        networkx_graph.add_edge(matrix[i][0], matrix[i][1], weight=matrix[i][2])


def path_compartmentalization(pseudo_path, compartmentalize_path):
    for i in range(len(pseudo_path) - 1):
        temp_array = []
        temp_array.append(pseudo_path[i])
        temp_array.append(pseudo_path[i + 1])
        compartmentalize_path.append(temp_array)


def pseudo_edge_checker(compartmentalize_path, edge_checker, networkx_graph):
    for i in range(len(compartmentalize_path)):
        temp_tuple = tuple(compartmentalize_path[i])
        edge_checker.append(networkx_graph.has_edge(*temp_tuple))


def pseudo2actual(compartmentalize_path, edge_checker, networkx_graph):
    for i in range(len(compartmentalize_path)):
        if not edge_checker[i]:
            compartmentalize_path[i] = nx.dijkstra_path(networkx_graph, compartmentalize_path[i][0],
                                                        compartmentalize_path[i][1])


def combine2actual(compartmentalize_path, actual_path):
    for i in range(len(compartmentalize_path)):
        length_of_path = len(compartmentalize_path[i])
        for j in range(length_of_path - 1):
            actual_path.append(compartmentalize_path[i][j])


def intra_uniqueness(target_list):
    unique_list = []
    for i in range(len(target_list)):
        if target_list[i] in unique_list:
            continue
        else:
            unique_list.append(target_list[i])
    return unique_list


def check_all_nodes_exist(list_of_all_nodes, list_to_check):
    new_list_of_all_nodes = copy.deepcopy(list_of_all_nodes)
    new_list_of_all_nodes.sort()
    new_list_to_check = []
    if list_to_check is list:
        for i in range(len(list_to_check)):
            for j in range(len(list_to_check[i])):
                new_list_to_check.append(list_to_check[i][j])
    else:
        for i in range(len(list_to_check)):
            new_list_to_check.append(list_to_check[i])
    new_list_to_check.sort()
    if new_list_of_all_nodes == new_list_to_check:
        return 0
    else:
        return 1


def begin_source_node(path_list, source_node_number):
    if path_list[0] != source_node_number:
        # find index of source node + make sure it exist
        try:
            source_index = path_list.index(source_node_number)
        except:
            source_index = 0
            path_list.insert(source_index, source_node_number)
        # split string
        back_nodes = path_list[:source_index]
        path_list = path_list[source_index:]
        path_list.extend(back_nodes)
    return path_list


def uniqueness_operator(groups, list_of_nodes):
    # intra-group uniqueness
    for i in range(len(groups)):
        groups[i] = intra_uniqueness(groups[i])
    # inter-group uniqueness
    for i in range(len(groups) - 1):
        for j in range(i + 1, len(groups)):
            intersection = list(set(groups[i]).intersection(groups[j]))
            # check intersection exists, if exists, remove intersection depending on the size
            for k in range(len(intersection)):
                bigger_group = 0
                if len(groups[i]) > len(groups[j]):
                    bigger_group = i
                elif len(groups[i]) < len(groups[j]):
                    bigger_group = j
                elif len(groups[i]) == len(groups[j]):
                    bigger_group = random.choice([i, j])
                groups[bigger_group].remove(intersection[k])
    # Make sure all vertices exist
    vertex_array = []
    for i in range(len(groups)):
        for j in range(len(groups[i])):
            if groups[i][j] not in vertex_array:
                vertex_array.append(groups[i][j])
    check_value = check_all_nodes_exist(list_of_nodes, vertex_array)
    if check_value == 1:
        return "UTF"
    else:
        return groups


def apply_crossover(number_of_groups, list_of_nodes,
                    crossover_optimization=None):
    groups = []
    if number_of_groups != 1:
        crossover_points = []
        while len(crossover_points) != (number_of_groups - 1):
            random_crossover_point = random.randint(1, len(list_of_nodes) - 1)
            if random_crossover_point not in crossover_points:
                crossover_points.append(random_crossover_point)
        crossover_points.sort()
        # add crossover optimization
        if crossover_optimization is not None:
            if crossover_points in crossover_optimization:
                return "OPT"
            else:
                crossover_optimization.append(crossover_points)
        # produce groups
        if len(crossover_points) != 1:
            for i in range(len(crossover_points)):
                temp_group = []
                if i == 0:
                    temp_group.extend(list_of_nodes[:crossover_points[i + 1]])
                else:
                    temp_group.extend(list_of_nodes[crossover_points[i - 1]:crossover_points[i]])
                groups.append(temp_group)
                if i == len(crossover_points) - 1:
                    temp_group = []
                    temp_group.extend(list_of_nodes[crossover_points[i]:])
                    groups.append(temp_group)
        elif len(crossover_points) == 1:
            groups.append(list_of_nodes[:crossover_points[0]])
            groups.append(list_of_nodes[crossover_points[0]:])
    else:
        groups.append(list_of_nodes)
    return groups


def fault_optimizer(mtsp_output, iteration_counter):
    if mtsp_output == "UTF" or mtsp_output == "OPT" or mtsp_output == "IVG":
        if mtsp_output == "UTF":
            print("Union Condition failed")
            iteration_counter += 1
        elif mtsp_output == "OPT":
            print("Detected Duplicate Crossover - Optimized!")
            iteration_counter += 1
        elif mtsp_output == "IVG":
            print("Invalid Group Member Size")
        return True, iteration_counter
    else:
        return False, iteration_counter


def calculate_distance(path, networkx_graph):
    total_length = 0
    for i in range(len(path) - 1):
        total_length += networkx_graph[path[i]][path[i + 1]]["weight"]
    return total_length


def nCr(n, r):
    f = math.factorial
    return f(n) / f(r) / f(n - r)


def mTSP(list_of_nodes, source_node_number, number_of_groups, networkx_graph, crossover_optimization=None):
    groups = apply_crossover(number_of_groups=number_of_groups, list_of_nodes=list_of_nodes,
                             crossover_optimization=crossover_optimization)
    if groups == "OPT":
        return "OPT"
    original_list = intra_uniqueness(list_of_nodes)
    groups = uniqueness_operator(groups, original_list)
    if groups == "UTF":
        return "UTF"
    # ensure no empty/ single group member
    invalid_group = False
    for i in range(len(groups)):
        if len(groups[i]) <= 1:
            invalid_group = True
    if invalid_group:
        return "IVG"
    # make sure all start from source node
    for i in range(len(groups)):
        if groups[i][0] != 0:
            groups[i].insert(0, source_node_number)
    matrix_array = [[] for i in range(len(groups))]
    # initialize cost matrix for each group
    for i in range(len(groups)):
        temp_array = []
        for j in range(len(groups[i])):
            temp_array.append([0 for k in range(len(groups[i]))])
        matrix_array[i] = temp_array
    # fill in cost matrix
    for i in range(len(matrix_array)):
        for j in range(len(matrix_array[i])):
            for k in range(len(matrix_array[i])):
                if matrix_array[i][j][k] == 0:
                    shortest_path = round(nx.dijkstra_path_length(networkx_graph, groups[i][j], groups[i][k]), 1)
                    if shortest_path == 0:
                        continue
                    else:
                        matrix_array[i][j][k] = shortest_path
                        matrix_array[i][k][j] = shortest_path
    # TSP
    translated_pseudo_path = []
    for i in range(len(matrix_array)):
        indv_group_matrix = range(len(matrix_array[i]))
        matrix_dist_dict = {(j, k): matrix_array[i][j][k] for j in indv_group_matrix for k in indv_group_matrix}
        pseudo_path = tsp.tsp(indv_group_matrix, matrix_dist_dict)[1]
        # translator
        translated_group = []
        for n in range(len(pseudo_path)):
            new_index = pseudo_path[n]
            translated_group.append(groups[i][new_index])
        # ensure source node starts first
        translated_group = begin_source_node(translated_group, source_node_number)
        # add source node in back
        translated_group.append(source_node_number)
        translated_pseudo_path.append(translated_group)
    # compartmentalize the edges
    compartmentalize_group_path = []
    for i in range(len(translated_pseudo_path)):
        temp_compartment = []
        path_compartmentalization(translated_pseudo_path[i], temp_compartment)
        compartmentalize_group_path.append(temp_compartment)
    # make sure there is edge between two nodes
    edge_group_checker = []
    for i in range(len(compartmentalize_group_path)):
        temp_edge_compartment = []
        pseudo_edge_checker(compartmentalize_group_path[i], temp_edge_compartment, networkx_graph)
        edge_group_checker.append(temp_edge_compartment)
    # replace pseudo w/ actual
    for i in range(len(compartmentalize_group_path)):
        pseudo2actual(compartmentalize_group_path[i], edge_group_checker[i], networkx_graph)
    # combine compartment to actual
    actual_group_path = []
    for i in range(len(compartmentalize_group_path)):
        temp_actual_compartment = []
        combine2actual(compartmentalize_group_path[i], temp_actual_compartment)
        actual_group_path.append(temp_actual_compartment)
    # check if returns to source node
    for i in range(len(actual_group_path)):
        if len(actual_group_path[i]) != 0:
            if actual_group_path[i][len(actual_group_path[i]) - 1] != source_node_number:
                actual_group_path[i].append(source_node_number)
        else:
            actual_group_path[i].append(source_node_number)
    # calculate total length
    total_length = 0
    for i in range(len(actual_group_path)):
        group_total_length = 0
        for j in range(len(actual_group_path[i]) - 1):
            group_total_length += networkx_graph[actual_group_path[i][j]][actual_group_path[i][j + 1]]["weight"]
        total_length += group_total_length
    return [total_length, actual_group_path]


def MmTSP(list_of_nodes, depots_node, number_of_robots, networkx_graph, minMaxReq=[]):
    single_robot_mtsp = mTSP(list_of_nodes, depots_node[0], 1, networkx_graph)
    single_robot_tour = single_robot_mtsp[1][0]
    # find index of depots
    depot_index_list = []
    for i in range(len(depots_node)):
        depot_index = single_robot_tour.index(depots_node[i])
        depot_index_list.append(depot_index)
    depot_index_list.sort()
    # slice deports accordingly
    depot_groups = []
    if len(depot_index_list) > 1:
        for i in range(1, len(depot_index_list)):
            start_node = depot_index_list[i - 1]
            end_node = depot_index_list[i]
            temp_groups = single_robot_tour[start_node:end_node]
            depot_groups.append(temp_groups)
            if i == len(depot_index_list) - 1:
                last_slice = single_robot_tour[end_node:]
                depot_groups.append(last_slice)
    else:
        depot_groups.append(single_robot_tour)
    # make sure each group does not have the other depot
    for i in range(len(depots_node)):
        for j in range(len(depots_node)):
            if i == j:
                continue
            try:
                depot_groups[i].remove(depots_node[j])
            except:
                continue
    # apply uniqueness operator
    depot_groups = uniqueness_operator(depot_groups, list_of_nodes)
    # ensure no group has only one node
    single_member_group = False
    for i in range(len(depot_groups)):
        if len(depot_groups[i]) == 1 or len(depot_groups[i]) == 0:
            single_member_group = True
    if single_member_group:
        print("Single Member Group has Failed")
        return "SMG"
    # sort depot groups by length
    depot_groups.sort(key=len, reverse=True)
    print("The unique depot node solution is:")
    print(depot_groups)
    # ensure the minimum number of element for each depot group
    for i in range(len(depot_groups)):
        if (len(depot_groups[i]) * 2) < number_of_robots[i]:
            print("Depot Group to Small")
            print("Depot in question:", depot_groups[i])
            print("Number of Robots:", number_of_robots[i])
            return "DGS"
    universal_group = []
    universal_crossover = []
    for i in range(len(depots_node)):
        universal_group.append({})
        universal_crossover.append([])
    number_of_iterations = 100
    for i in range(len(depots_node)):
        print("Depot: ", depots_node[i])
        iteration_counter = 0
        while iteration_counter < number_of_iterations:
            if number_of_robots[i] == 1:
                iteration_counter = number_of_iterations - 1
            mtsp_output = mTSP(depot_groups[i], depots_node[i], number_of_robots[i], networkx_graph,
                               universal_crossover[i])
            fault_flag, iteration_counter = fault_optimizer(mtsp_output, iteration_counter)
            if fault_flag:
                continue
            total_length = mtsp_output[0]
            actual_group_path = mtsp_output[1]
            if total_length not in universal_group[i]:
                universal_group[i][total_length] = [actual_group_path]
            else:
                universal_group[i][total_length].append(actual_group_path)
            iteration_counter += 1
    empty_dict = False
    for i in range(len(universal_group)):
        if len(universal_group[i]) == 0:
            empty_dict = True
    if empty_dict:
        print("Empty Dictionary has been Detected")
        return "ED"
    final_tour = []
    for i in range(len(universal_group)):
        dic_keys = list(universal_group[i].keys())
        path_and_length = []
        if len(minMaxReq) == 0:
            smallest_tour = min(dic_keys)
            if len(universal_group[i][smallest_tour]) > 1:
                random_index = random.randint(0, len(universal_group[i][smallest_tour]) - 1)
                path_and_length.append(universal_group[i][smallest_tour][random_index])
            else:
                path_and_length.append(universal_group[i][smallest_tour][0])
            path_and_length.append(smallest_tour)
        else:
            minDistance = minMaxReq[0]
            maxDistance = minMaxReq[1]
            dic_keys.sort()
            for j in range(len(dic_keys)):
                temp_key = dic_keys[j]
                temp_path = universal_group[i][temp_key]
                validDistance = True
                # make sure distance checks out
                for k in range(len(temp_path[0])):
                    tempDistance = calculate_distance(temp_path[0][k], networkx_graph)
                    if tempDistance < minDistance or tempDistance > maxDistance:
                        validDistance = False
                        break
                if validDistance:
                    path_and_length.append(universal_group[i][temp_key][0])
                    break
            if validDistance:
                path_and_length.append(temp_key)
        if len(path_and_length) != 0:
            final_tour.append(path_and_length)

    if len(final_tour) != len(depots_node):
        return "NS"

    return final_tour
