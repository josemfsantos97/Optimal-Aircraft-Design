%% Initialize

clear all
close all
clc
scrsz=get(0,'ScreenSize');

%% Function f(x)

func = @(x1,x2)(100*(x2-x1.^2).^2+(1-x1.^2));

%% Plot f(x)

x1_i = -2;
x1_f = 3;
x2_i= -2;
x2_f=3;
nx1 = 500;
nx2= 500;

x1_vector = linspace(x1_i,x1_f,nx1);
x2_vector = linspace(x2_i,x2_f,nx2);

[x1,x2] = meshgrid(x1_vector,x2_vector);
zlevels = [1, 0.5 ,0.1, 0.01,0.001,5];

contour(x1,x2,func(x1,x2),25);
hold on
contour(x1,x2,func(x1,x2),zlevels,'ShowText','on')

%% Inequality

ineq = x1+x2<0;
f=double(ineq);
hold on
contour(x1,x2,f)
view(0,90)

%% Filling area
vertices_x = [-2,-2,3,3,2];
vertices_y = [2,3,3,-2,-2];
a=fill(vertices_x, vertices_y,'r');
alpha(a,0.4);

% z = func(x1,x2);
% minimum = min(min(z));
% [x1_pos,x2_pos]=find(z==minimum);
% x1_vector(x1_pos);
% x2_vector(x2_pos);
% plot(x1_vector(x1_pos),x2_vector(x2_pos),'*r');

%% Minimization with fminunc
func = @(x)(100*(x(2)-x(1)^2)^2+(1-x(1))^2);
x0= [2,2];
options = optimoptions(@fminunc,'Display','iter','Algorithm','quasi-newton');
[pos_opt,f_opt] = fminunc(func,x0,options);
plot(pos_opt(1),pos_opt(2),'*r')


%% Minimization with fmincon
A= [1,1];
b=0;
x = fmincon(func,x0,A,b);
plot(x(1),x(2),'*r')





