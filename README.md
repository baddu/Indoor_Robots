# Indoor_Robots
Generalized Task Allocation and Route Planning for Multiple Robots with Multiple Depots in Indoor Building Environments

# Name of Project

## Introduction
This project is comprised of four main files, with the following functionality:
* robotTourUtil.py: contains necessary operations in mTSP and MmTSP. and the functions themselves
* mTSP.py: contains an example of mTSP
* fMmTSP.py: contains an example of fMmTSP
* depotOptimizer.py: utilizes fMmTSP to find the optimal depots, given the number of depots, and number of robots per depot

Among the four files, three can be independently ran by itself. More details of such files are provided in the sections below. Note, all these function run on a given graph, defined in robotTourUtil.py. If you want to change it, you will have to modify the variable, _"matrix_input"_.

## mTSP.py
The "_mTSP_main_" function (contained in mTSP.py) requires one parameter - the number of robots. Currently, when running the mTSP.py file, it will return the optimal tour, given two robots in starting point 0, under 100 iterations. You can modify the starting point and number of iterations by changing the variable: "_source_node_number_" for starting point, and "_number_of_iterations_" for the number of iterations. To modify the number of robots in one depot, change the parameter of the "_mTSP_main_" function.

## fMmTSP.py
The fMmTSP.py file provides an example using the _MmTSP_ function defined in robotTourUtil.py. Such function requires four parameters:
* _list_of_nodes_: essentially an array containing all nodes in the graph, _G_
* _depots_node_: an array containing the starting nodes (must exist in graph, _G_)
* _number_of_robots_: an array containing number of robots in each node; the nodes are referred via index (index _J_ in _number_of_robots_ refers to the number of robots in depot _J_ in _depots_node_)
* _G_: the graph itself

## depotOptimizer.py
This file finds the optimal depot, given the number of depots and number of robots in each depot. The file, when run, requires users to input the number of depots, and the number of iterations. To modify the number of robots per depot, modify the variable "_number_of_robots_" in the source code. Note, there will also be different iterations when running each mTSP. To change that, go to robotTourUtil.py and change "_number_of_iterations_" in the MmTSP function.
