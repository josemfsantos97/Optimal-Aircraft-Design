import numpy as np
import openmdao as openmdao

from openaerostruct.geometry.utils import generate_mesh
from openaerostruct.integration.aerostruct_groups import AerostructGeometry, AerostructPoint
from openaerostruct.utils.constants import grav_constant

from openmdao.api import IndepVarComp, Problem, Group, SqliteRecorder

# Create a dictionary to store options about the surface
mesh_dict = {'num_y' : 17,
             'num_x' : 3,
             'wing_type' : 'CRM',
             'symmetry' : True,
             'num_twist_cp' : 5}

mesh, twist_cp = generate_mesh(mesh_dict)

surf_dict = {
            # Wing definition
            'name' : 'wing',        # name of the surface
            'symmetry' : True,     # if true, model one half of wing
                                    # reflected across the plane y = 0
            'S_ref_type' : 'wetted', # how we compute the wing area,
                                     # can be 'wetted' or 'projected'
            'fem_model_type' : 'tube',
            'chord_cp':np.ones(5)*5,
            'thickness_cp' : np.array([.1, .2, .3]),
            'taper_ratio' : 0.3,
            'dihedral':np.zeros(4),
            'span' :23.24,
            'twist_cp' : twist_cp,
            'mesh' : mesh,
            'sweep':15,
            # Aerodynamic performance of the lifting surface at
            # an angle of attack of 0 (alpha=0).
            # These CL0 and CD0 values are added to the CL and CD
            # obtained from aerodynamic analysis of the surface to get
            # the total CL and CD.
            # These CL0 and CD0 values do not vary wrt alpha.
            'CL0' : 0.1,            # CL of the surface at alpha=0
            'CD0' : 0.0078,            # CD of the surface at alpha=0

            # Airfoil properties for viscous drag calculation
            'k_lam' : 0.05,         # percentage of chord with laminar
                                    # flow, used for viscous drag
            't_over_c_cp' : np.array([0.08, 0.08, 0.10, 0.08]),      # thickness over chord ratio (NACA0015)
            'c_max_t' : .37,       # chordwise location of maximum (NACA0015)
                                    # thickness
            'with_viscous' : True,
            'with_wave' : False,     # if true, compute wave drag

            # Structural values are based on aluminum 7075
            'E' : 71.7e9,              # [Pa] Young's modulus
            'G' : 26.9e9,     # [Pa] shear modulus (calculated using E and the Poisson's ratio here)
            'yield' : (503.e6 / 1.5),  # [Pa] allowable yield stress
            'mrho' : 2810,           # [kg/m^3] material density
            'fem_origin' : 0.35,    # normalized chordwise location of the spar
            'wing_weight_ratio' : 1.25,
            'struct_weight_relief' : False,    # True to add the weight of the structure to the loads on the structure
            'distributed_fuel_weight' : False,
            # Constraints
            'exact_failure_constraint' : False, # if false, use KS function
            'fuel_density' : 803.,      # [kg/m^3] fuel density (only needed if the fuel-in-wing volume constraint is used)

            }

# Create a dictionary to store options about the surface
# Create a dictionary to store options about the surface
mesh_dict = {'num_y' : 17,
             'num_x' : 3,
             'wing_type' : 'rect',
             'symmetry' : True,
             'num_twist_cp' : 3,
             'offset' : np.array([50, 0., 0.])}

mesh= generate_mesh(mesh_dict)

surf_dict2 = {
            # Wing definition
            'name' : 'tail',        # name of the surface
            'symmetry' : True,     # if true, model one half of wing
                                    # reflected across the plane y = 0
            'twist_cp' : twist_cp,
            'S_ref_type' : 'wetted', # how we compute the wing area,
                                     # can be 'wetted' or 'projected'
            'fem_model_type': 'tube',
            'mesh' : mesh,
            'thickness_cp' : np.array([.1, .2, .3]),
            'span':8.,
            't_over_c_cp' : np.array([0.15]),      # thickness over chord ratio (NACA0015)
            # Aerodynamic performance of the lifting surface at
            # an angle of attack of 0 (alpha=0).
            # These CL0 and CD0 values are added to the CL and CD
            # obtained from aerodynamic analysis of the surface to get
            # the total CL and CD.
            # These CL0 and CD0 values do not vary wrt alpha.
            'CL0' : 0.0,            # CL of the surface at alpha=0
            'CD0' : 0.015,            # CD of the surface at alpha=0

            # Airfoil properties for viscous drag calculation
            'k_lam' : 0.05,         # percentage of chord with laminar
                                    # flow, used for viscous drag
            'c_max_t' : .30,       # chordwise location of maximum (NACA0015)
                                    # thickness
            'with_viscous' : True,
            'with_wave' : False,     # if true, compute wave drag

            'E' : 71.7e9,              # [Pa] Young's modulus
            'G' : 26.9e9,     # [Pa] shear modulus (calculated using E and the Poisson's ratio here)
            'yield' : (503.e6 / 1.5),  # [Pa] allowable yield stress
            'mrho' : 2810,           # [kg/m^3] material density
            'fem_origin' : 0.35,    # normalized chordwise location of the spar
            'wing_weight_ratio' : 1.25,
            'struct_weight_relief' : False,    # True to add the weight of the structure to the loads on the structure
            'distributed_fuel_weight' : False,
            # Constraints
            'exact_failure_constraint' : False, # if false, use KS function
            }
surfaces = [surf_dict, surf_dict2]
#surfaces= [surf_dict]


# Create the problem and assign the model group
prob = Problem()

# Add problem information as an independent variables component
indep_var_comp = IndepVarComp()
indep_var_comp.add_output('v', val=np.array([.78 * 297.72, .60 * 340.294]), units='m/s')
indep_var_comp.add_output('alpha', val=5., units='deg')
indep_var_comp.add_output('Mach_number', val=np.array([0.78, 0.60]))
indep_var_comp.add_output('re',val=np.array([0.3803*297.72*0.78*1./(1.43*1e-5), \
                          1.225*340.294*.60*1./(1.81206*1e-5)]),  units='1/m')
indep_var_comp.add_output('rho', val=np.array([0.3803, 1.225]), units='kg/m**3')
indep_var_comp.add_output('CT', val=0.38/3600, units='1/s')
indep_var_comp.add_output('R', val=3120620, units='m')
indep_var_comp.add_output('W0', val=19724.5,  units='kg')
indep_var_comp.add_output('speed_of_sound', val= np.array([297.72, 340.294]), units='m/s')
indep_var_comp.add_output('load_factor', val=np.array([1., 3.0]))
indep_var_comp.add_output('empty_cg', val=np.zeros((3)), units='m')
indep_var_comp.add_output('alpha_maneuver', val=0., units='deg')

prob.model.add_subsystem('prob_vars',
     indep_var_comp,
     promotes=['*'])


for surface in surfaces:
    name=surface['name']
    aerostruct_group = AerostructGeometry(surface=surface)
    prob.model.add_subsystem(name, aerostruct_group)

# Add tmp_group to the problem with the name of the surface.
for i in range(2):
    point_name = 'AS_point_{}'.format(i)
    
    # Create the aero point group and add it to the model
    AS_point = AerostructPoint(surfaces=surfaces)

    prob.model.add_subsystem(point_name, AS_point)
    
    prob.model.connect('v', point_name + '.v', src_indices=[i])
    prob.model.connect('Mach_number', point_name + '.Mach_number', src_indices=[i])
    prob.model.connect('re', point_name + '.re', src_indices=[i])
    prob.model.connect('rho', point_name + '.rho', src_indices=[i])
    prob.model.connect('CT', point_name + '.CT')
    prob.model.connect('R', point_name + '.R')
    prob.model.connect('W0', point_name + '.W0')
    prob.model.connect('speed_of_sound', point_name + '.speed_of_sound', src_indices=[i])
    prob.model.connect('empty_cg', point_name + '.empty_cg')
    prob.model.connect('load_factor', point_name + '.load_factor', src_indices=[i])  

    for surface in surfaces:
        name=surface['name']
        com_name = point_name + '.' + name + '_perf'
        prob.model.connect(name + '.local_stiff_transformed', point_name + '.coupled.' + name + '.local_stiff_transformed')
        prob.model.connect(name + '.nodes', point_name + '.coupled.' + name + '.nodes')

        # Connect aerodyamic mesh to coupled group mesh
        prob.model.connect(name + '.mesh', point_name + '.coupled.' + name + '.mesh')

        # Connect performance calculation variables
        prob.model.connect(name + '.radius', com_name + '.radius')
        prob.model.connect(name + '.thickness', com_name + '.thickness')
        prob.model.connect(name + '.nodes', com_name + '.nodes')
        prob.model.connect(name + '.cg_location', point_name + '.' + 'total_perf.' + name + '_cg_location')
        prob.model.connect(name + '.structural_mass', point_name + '.' + 'total_perf.' + name + '_structural_mass')
        prob.model.connect(name + '.t_over_c', com_name + '.t_over_c')
    

prob.model.connect('alpha','AS_point_0' + '.alpha')
prob.model.connect('alpha_maneuver', 'AS_point_1' + '.alpha')

from openmdao.api import ScipyOptimizeDriver
prob.driver = ScipyOptimizeDriver()
prob.driver.options['tol'] = 1e-6

recorder = SqliteRecorder("merda43.db")
prob.driver.add_recorder(recorder)
prob.driver.recording_options['record_derivatives'] = True
prob.driver.recording_options['includes'] = ['*']

# Setup problem and add design variables, constraint, and objective
prob.model.add_design_var('wing.twist_cp', lower=-10., upper=15.)
#prob.model.add_design_var('tail.twist_cp', lower=-10., upper=15.)
prob.model.add_design_var('wing.sweep', lower=-40., upper=50.)
prob.model.add_design_var('wing.thickness_cp', lower=0.01, upper=0.5, scaler=1e2)
prob.model.add_design_var('alpha', lower=-10., upper=10.)
prob.model.add_design_var('alpha_maneuver', lower=-15., upper=15)

#prob.model.add_design_var('wing.geometry.dihedral', lower=-10., upper=10.)

#prob.model.add_design_var('wing.radius',lower=0.05, upper=0.5)

prob.model.add_constraint('AS_point_1.wing_perf.failure', upper=0.)
prob.model.add_constraint('AS_point_1.wing_perf.thickness_intersects', upper=0.)
prob.model.add_constraint('AS_point_1.L_equals_W', equals=0.)
prob.model.add_constraint('AS_point_0.CL', equals=0.47)


UPPER=np.ones(5)*15
LOWER=np.ones(5)*-5
UPPER[-1]=0.0
LOWER[-1]=0.0

prob.model.add_constraint('wing.twist_cp', lower=LOWER , upper=UPPER)
# Add design variables, constraisnt, and objective on the problem
prob.model.add_objective('AS_point_0.fuelburn', scaler=1e-5)

# Set up the problem
prob.setup(check=True)
#openmdao.visualization.n2_viewer.n2_viewer.n2(prob.model, outfile='n22.html', show_browser=True, embeddable=False, title=None, use_declare_partial_info=False)

prob.run_driver()