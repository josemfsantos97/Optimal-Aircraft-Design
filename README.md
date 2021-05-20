
#  Aircraft Optimal Design
This repository contains files and brief explanation regarding the homework assignments for the course Aircraft Optimal Design. There are a total of 4 assignments in which the first 3 are solved in MatLab and consist of an introduction to optimization algorithms and the 4th one is solved in OpenAeroStruct (low-fidelity aerostructural wing design tool) which is built on top of OpenMDAO.

## [Homework01 - Gradient based optimization and Heuristic Optimization using a Generic Algorithm](https://github.com/josemfsantos97/Optimal-Aircraft-Design/tree/main/Homework01)
- Performing constrained and unconstrained optimization of the Rosenbrock function using Quasi-Newton (BFGS) method. Analysing and understanding gradient-based algorithms.
- Using a genetic algorithms to calculate the minimum of the Rosenbrock function and comparing computation cost with Quasi-Newton methods.

The Rosenbrock function:

<img src="https://github.com/josemfsantos97/Optimal-Aircraft-Design/blob/main/Homework01/images/1280px-Rosenbrock_function.png" width="450" />


The following figure shows a visual intrepretation for the genetic algorithm convergence. In the upper part it is possible to see how after 500 generations the algorithm seems to have converged and in the lower plot the average fitness value decreasing with the number of generations.

![Genetic Algorithm](https://github.com/josemfsantos97/Optimal-Aircraft-Design/blob/main/Homework01/images/gen1000size500.png)


## [Homework02  - Gradient based optimization and Finite Differences](https://github.com/josemfsantos97/Optimal-Aircraft-Design/tree/main/Homework02)
- Finding the global minimum of the Goldstein-Price function using several optimization algorithms and variations such as Quasi-Newton (DFP), Quasi-Newton (BFGS) and Steepest Descent. Furthermore, these algorithms are compared as well as their computational cost and effecacy, e.g., if they are able to reach the global minumum or get stuck in a local minimum.
- Sensitivity analysis of Finite Differences. How to calculate truncation error and how does it decay with the step size. The problem of subtractive cancellation errors.

<p float="left">
  <img src="https://github.com/josemfsantos97/Optimal-Aircraft-Design/blob/main/Homework02/images/steepest_descent.png" width="450" />
  <img src="https://github.com/josemfsantos97/Optimal-Aircraft-Design/blob/main/Homework02/images/steepest_descent2d.png" width="450" /> 
</p>

## [Homework03  - Introduction to OpenMDAO and OpenAeroStruct](https://github.com/josemfsantos97/Optimal-Aircraft-Design/tree/main/Homework03)
- Setting up the simple optimization problem already computed in the last homeworks (Rosenbrock function), this time using OpenMDAO. OpenMDAO is an open-source framework for efficient multidisciplinary optimization. Introduction to N2 diagrams.
- Understanding the simplified models used by OpenAeroStruct - vortex-lattice method and spatial beam model to simulate aerodynamic and structural analyses using lifting surfaces.
- Creating and incorporationg a function to calculate the Reynolds number that can be used as additional constraint.
- Solving a typical aerodynamic optimization problem of an isolated aircraft wing given by:

![Optimization problem](https://github.com/josemfsantos97/Optimal-Aircraft-Design/blob/main/Homework03/images/optimization_prob_tt3.png)

Some results:

<p float="left">
  <img src="https://github.com/josemfsantos97/Optimal-Aircraft-Design/blob/main/Homework03/images/n2_constrained.png" width="400" />
  <img src="https://github.com/josemfsantos97/Optimal-Aircraft-Design/blob/main/Homework03/images/viscous.png" width="550" /> 
</p>
