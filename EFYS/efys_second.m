syms x y;

% Define the function
f = 3*x^2 - y;

% Create the vector [x, y]
v = [x, y];

% Compute the gradient
g = gradient(f, v);

% Define a grid for x and y values
[X, Y] = meshgrid(-1:0.1:1, -1:0.1:1);

% Evaluate the gradient at each point in the grid
Gx = double(subs(g(1), {x, y}, {X, Y}));
Gy = double(subs(g(2), {x, y}, {X, Y}));

% Create a figure
figure;

% Plot the gradient vector field using quiver
quiver(X, Y, Gx, Gy, 'AutoScale', 'on', 'AutoScaleFactor', 2);

% Set axis labels
xlabel('X');
ylabel('Y');

% Add a title
title('Gradient Vector Field');

% Show the grid
grid on;

% Show the plot
hold off;


clear;
syms x y;

% Define the function
f = 3*x^2 - y*x;

% Create the vector [x, y]
v = [x, y];

% Compute the gradient
g = gradient(f, v);

% Define a grid for x and y values
[X, Y] = meshgrid(-1:0.1:1, -1:0.1:1);

% Evaluate the gradient at each point in the grid
Gx = double(subs(g(1), {x, y}, {X, Y}));
Gy = double(subs(g(2), {x, y}, {X, Y}));

% Create a figure
figure;

% Plot the gradient vector field using quiver
quiver(X, Y, Gx, Gy, 'AutoScale', 'on', 'AutoScaleFactor', 2);

% Set axis labels
xlabel('X');
ylabel('Y');

% Add a title
title('Gradient Vector Field');

% Show the grid
grid on;

% Show the plot
hold off;




