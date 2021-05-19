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
