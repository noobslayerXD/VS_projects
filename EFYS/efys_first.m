% Vectors
a = [1 2 3];
b = [4 5 6];

% Cross products
c_ab = cross(b, a);
c_ba = cross(a, b);

% Norms
norm_a = norm(a);
norm_b = norm(b);

% Dot product and angle calculation
dot_product = dot(a, b);
angle_rad = acos(dot_product / (norm_a * norm_b));
angle_deg = rad2deg(angle_rad);

% Create a figure
figure;

% Plot the vectors using quiver3
quiver3(0, 0, 0, a(1), a(2), a(3), 'r', 'LineWidth', 2); hold on;
quiver3(0, 0, 0, b(1), b(2), b(3), 'b', 'LineWidth', 2);
quiver3(0, 0, 0, c_ab(1), c_ab(2), c_ab(3), 'g', 'LineWidth', 2);
quiver3(0, 0, 0, c_ba(1), c_ba(2), c_ba(3), 'm', 'LineWidth', 2);

% Set axis labels
xlabel('X');
ylabel('Y');
zlabel('Z');

% Set axis limits based on vector magnitudes
axis([-max(norm_a, norm_b), max(norm_a, norm_b), -max(norm_a, norm_b), max(norm_a, norm_b), -max(norm_a, norm_b), max(norm_a, norm_b)]);

% Set aspect ratio to be equal
axis equal;

% Add a legend
legend('Vector a', 'Vector b', 'Cross product (b x a)', 'Cross product (a x b)');

% Show the angle and dot product information
title(['Angle between a and b: ' num2str(angle_deg) ' degrees, Dot Product: ' num2str(dot_product)]);

% Show the grid
grid on;

% Show the plot
hold off;
