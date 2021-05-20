"""
Created on Wed Nov 20 01:33:53 2019<

@author: josem


Demonstration of a model using the Paraboloid component.
"""

from __future__ import division, print_function

import openmdao
import openmdao.api as om
from openmdao.devtools import itrace as tool
from openmdao.devtools import iprofile as tool


class Rosenbrock(om.ExplicitComponent):
    """
    Evaluates the equation f(x,y) = (x-3)^2 + xy + (y+4)^2 - 3.
    """

    def setup(self):
        self.add_input('x', val=0.0)
        self.add_input('y', val=0.0)

        self.add_output('f_xy', val=0.0)

        """ Finite difference or analytical"""
        #self.declare_partials('*', '*', method='fd')
        
        self.declare_partials('f_xy', 'x')
        self.declare_partials('f_xy', 'y')

        
    def compute(self, inputs, outputs):
        """
        f(x,y) = (x-3)^2 + xy + (y+4)^2 - 3

        Minimum at: x = 1.00; y = 1.00
        """
        x = inputs['x']
        y = inputs['y']

        outputs['f_xy'] = (1.0-x)**2.0 + 100.0*(y-x**2.0)**2.0
        
    def compute_partials(self, inputs, partials):
        x = inputs['x']
        y = inputs['y']

        partials['f_xy', 'x']=400*x**3+2*x-400*x*y-2
        partials['f_xy', 'y']=200*y-200*x**2


prob = om.Problem()

indeps = prob.model.add_subsystem('indeps', om.IndepVarComp())
indeps.add_output('x')
indeps.add_output('y')

prob.model.add_subsystem('rosen', Rosenbrock())

# define the component whose output will be constrained
prob.model.add_subsystem('const', om.ExecComp('g = x + y'))

# prob.model.connect('indeps.x', ['rosen.x','const.x'])
# prob.model.connect('indeps.y', ['rosen.y','const.y'])

prob.model.connect('indeps.x', 'rosen.x')
prob.model.connect('indeps.y', 'rosen.y')

# setup the optimization
prob.driver = om.ScipyOptimizeDriver()
#prob.driver.options['optimizer'] = 'COBYLA'

prob.model.add_design_var('indeps.x', lower=-50, upper=50)
prob.model.add_design_var('indeps.y', lower=-50, upper=50)
prob.model.add_objective('rosen.f_xy')

# to add the constraint to the model
# prob.model.add_constraint('const.g', upper=1)
#prob.model.add_constraint('const.g', equals=0.)

# turn on profiling
tool.start()
prob.setup()

# set initial values 
prob.set_val('indeps.x', 3.4)
prob.set_val('indeps.y', 2.2)

prob.run_driver()
tool.stop()

#data = prob.check_partials()
#x_error = data['rosen']['f_xy', 'x']['rel error']
#y_error = data['rosen']['f_xy', 'y']['rel error']

print('Function value: {:.5f} at ({:.2f},{:.2f})'.format(*prob['rosen.f_xy'], *prob['indeps.x'], *prob['indeps.y']))


#openmdao.visualization.n2_viewer.n2_viewer.n2(prob.model, outfile='rosenbrock_n2.html', show_browser=True, embeddable=False, title=None, use_declare_partial_info=False)
