%% Initialize

clear all
close all
clc
scrsz=get(0,'ScreenSize');

%% Function f(x)

func = @(x)(100*(x(2)-x(1)^2)^2+(1-x(1))^2);


%% Minimization using genetic algorithm

problem.fitnessfcn = func;
problem.nvars = 2;
problem.options = optimoptions('ga','PlotFcn',{@RosenbrockPlotIterates,@gaplotbestf},'PopulationSize',500);
% problem.options = optimoptions('ga','PlotFcn',@rastriginsPlotIterates,...
%                       'PopulationSize',100,'PlotFcn',@gaplotbestf,...
%                       'MaxGenerations',500,'MaxStallGenerations', 500,'InitialPopulation',X0);


[x,Fval,exitFlag,Output]=ga(problem)
% [x,Fval,exitFlag,Output] = ga(problem);
hold on 
% plot(x(1),x(2),'MarkerSize',25,'Marker','*','Color',[1 0 0]);
% rosenbrockfcnCont()
hold off


