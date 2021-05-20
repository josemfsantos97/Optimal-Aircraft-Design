import numpy as np

from openmdao.api import IndepVarComp, Problem, Group, NewtonSolver, ScipyKrylov, LinearBlockGS, NonlinearBlockGS, DirectSolver, PETScKrylov, SqliteRecorder

from openaerostruct.geometry.utils import generate_mesh
from openaerostruct.geometry.geometry_group import Geometry
from openaerostruct.aerodynamics.aero_groups import AeroPoint
from openaerostruct.aerodynamics.lift_coeff_2D import LiftCoeff2D


# Create a dictionary to store options about the mesh
mesh_dict = {'num_y' : 25,
             'num_x' : 7,
             'wing_type' : 'rect',
             'symmetry' : True,
             'num_twist_cp' : 5}

# Generate the aerodynamic mesh based on the previous dictionary
mesh = generate_mesh(mesh_dict)
# Create a dictionary with info and options about the aerodynamic
# lifting surface
surface = {
            # Wing definition
            'name' : 'wing',        # name of the surface
            'symmetry' : True,     # if true, model one half of wing
                                    # reflected across the plane y = 0
            'S_ref_type' : 'wetted', # how we compute the wing area,
                                     # can be 'wetted' or 'projected'
            'fem_model_type' : 'tube',

            'twist_cp' : np.zeros(5),
            'chord_cp' : np.ones(3)*1.47,
            
            'mesh' : mesh,

            # Aerodynamic performance of the lifting surface at
            # an angle of attack of 0 (alpha=0).
            # These CL0 and CD0 values are added to the CL and CD
            # obtained from aerodynamic analysis of the surface to get
            # the total CL and CD.
            # These CL0 and CD0 values do not vary wrt alpha.
            'CL0' : 0.09,            # CL of the surface at alpha=0
            'CD0' : 0.00225,            # CD of the surface at alpha=0

            # Airfoil properties for viscous drag calculation
            'k_lam' : 0.05,         # percentage of chord with laminar
                                    # flow, used for viscous drag
            't_over_c_cp' : np.array([0.12]),      # thickness over chord ratio (NACA2412)
            'c_max_t' : .30,       # chordwise location of maximum (NACA2412)
                                    # thickness
            'with_viscous' : True,  # if true, compute viscous drag
            'with_wave' : False,     # if true, compute wave drag
            }

# Create the OpenMDAO problem
prob = Problem()

# Create an independent variable component that will supply the flow
# conditions to the problem.
indep_var_comp = IndepVarComp()
indep_var_comp.add_output('v', val=63, units='m/s')
indep_var_comp.add_output('alpha', val=5., units='deg')
indep_var_comp.add_output('Mach_number', val=0.19)
indep_var_comp.add_output('miu', val=0.00001726, units='N*s/m**2')
indep_var_comp.add_output('rho', val=1.007, units='kg/m**3')
indep_var_comp.add_output('cg', val=np.zeros((3)), units='m')
#indep_var_comp.add_output('re', val = Rec, units ='1')

# Add this IndepVarComp to the problem model
prob.model.add_subsystem('prob_vars',
    indep_var_comp,
    promotes=['*'])

# Create and add a group that handles the geometry for the
# aerodynamic lifting surface
geom_group = Geometry(surface=surface)
prob.model.add_subsystem(surface['name'], geom_group)

# Create the aero point group, which contains the actual aerodynamic
# analyses
aero_group = AeroPoint(surfaces=[surface], user_specified_Sref = True)
point_name = 'aero_point_0'
prob.model.add_subsystem(point_name, aero_group,
promotes_inputs=['v', 'alpha', 'Mach_number', 'rho', 'cg','miu'])

name = surface['name']

# Connect the mesh from the geometry component to the analysis point
prob.model.connect(name + '.mesh', point_name + '.' + name + '.def_mesh')

# Perform the connections with the modified names within the
# 'aero_states' group.
prob.model.connect(name + '.mesh', point_name + '.aero_states.' + name + '_def_mesh')
prob.model.connect(name + '.t_over_c', point_name + '.' + name + '_perf.' + 't_over_c')

# Import the Scipy Optimizer and set the driver of the problem to use
# it, which defaults to an SLSQP optimization method
from openmdao.api import ScipyOptimizeDriver
prob.driver = ScipyOptimizeDriver()
prob.driver.options['tol'] = 1e-9

recorder = SqliteRecorder("aero_aero.db")
prob.driver.add_recorder(recorder)
prob.driver.recording_options['record_derivatives'] = True
prob.driver.recording_options['includes'] = ['*']

UPPER=np.ones(5)*10000
LOWER=np.ones(5)*-10000
UPPER[-1]=0.0
LOWER[-1]=0.0

#prob.model.connect(name + '.chord_cp', point_name + '.' + name + '_perf.' + 'Rec')
# Setup problem and add design variables, constraint, and objective
prob.model.add_design_var('wing.twist_cp', lower=-10., upper=10.) 
prob.model.add_design_var('alpha', lower=-10., upper=15.)
prob.model.add_design_var('wing.chord_cp', lower=0, upper=20.)

prob.model.add_constraint('wing.twist_cp', lower=LOWER , upper=UPPER)
prob.model.add_constraint(point_name + '.wing_perf.CL', equals=0.33)
prob.model.add_constraint(point_name + '.wing_perf.Cl', lower = 0.0, upper = 1.6)
prob.model.add_constraint(point_name + '.wing.S_ref', equals = 16.2)
prob.model.add_objective(point_name + '.wing_perf.CD', scaler=1e4)
prob.model.add_constraint(point_name + '.wing_perf.Rec',lower = 5E6)

# Set up and run the optimization problem
prob.setup()
# prob.check_partials(compact_print=True)
# exit()
prob.run_driver()
prob.record_iteration('final')
prob.cleanup()

print('alpha \n')
print(prob['alpha'], '\n')

print('chord \n')
print(prob['wing.chord_cp'], '\n')

print('twist \n')
print(prob['wing.twist_cp'], '\n')

print('CD \n')
print(prob['aero_point_0.wing_perf.CD'], '\n')

print('CL \n')
print(prob['aero_point_0.wing_perf.CL'], '\n')

print('Cl \n')
print(prob['aero_point_0.wing_perf.Cl'], '\n')

print('S_ref \n')
print(prob['aero_point_0.wing.S_ref'], '\n')

print('Re\n')
print(prob['aero_point_0.wing_perf.Rec'], '\n')