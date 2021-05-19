function state = RosenbrockPlotIterates(options,state,flag)
% Helper function for rastrigins optimization
i=0;
%  Copyright (c) 2010, The MathWorks, Inc.
%  All rights reserved.

% Plot each individual using a small black star
plot(state.Population(:,1),state.Population(:,2),'k*');
hold on;
% Plot underlying contour plot of surface

axis([-2,3,-2,3]);
hold off
pause(0.05)

