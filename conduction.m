clc, clear, close all
%% Active parameters

% 
% degree_build = deg2rad(0:1:360);
% window_size = 0:0.1:1; %Ratio
% isolation = 

degree_build = deg2rad(45);
window_size = 0.8; %Ratio
isolation = 0.5;

%% Constants
int_temp = 22.0;
I_r = readmatrix('Radiation_Data_Zurich_2018.csv');
T_out = readmatrix('Temp_Data_Basel_2021.csv');
sun_angle= deg2rad(readmatrix('Zenith_Angle_Data_Zurich_2018.csv'));


month_temp_idx = [1, 745, 1415, 2161, 2881, 3625, 4345, 5089, 5833, 6553, 7297, 8017, 8760];

A_wall = (1-window_size)*100;
A_wind = 100*window_size;

A_wall_exposed = A_wall/4 * cos(degree_build) + A_wall/4 * sin(degree_build);

A_wind_exposed = A_wind/4 * cos(degree_build) + A_wind/4 * sin(degree_build);

z = 0.68;
ws = 0.7;

Eps_s = 0.6;

J2kwh = 2.77778*10^(-7);
Th_cond_wall = 1.2;
Th_cond_window = 0.7;
e_window = 0.1;
timestep = 60*60;
air_coeff = 3;


E_loss_cond = zeros(12,1);
E_sun = zeros(12,1);


for i=1:12
    Q_wall = abs( Eps_s .* A_wall_exposed.* I_r(month_temp_idx(i):month_temp_idx(i+1)).* cos(sun_angle(month_temp_idx(i):month_temp_idx(i+1))));
    T_we = (Q_wall+Th_cond_wall./isolation .* A_wall .* int_temp + air_coeff.*A_wall.*T_out(month_temp_idx(i):month_temp_idx(i+1))) ./ (Th_cond_wall./isolation .* A_wall+air_coeff.*A_wall);
    %T_we = T_out(month_temp_idx(i):month_temp_idx(i+1));
    Q_loss = Th_cond_wall./isolation .* A_wall .* (T_we - int_temp) + Th_cond_window./e_window .* A_wind .*(T_we - int_temp);
    Q_sun = abs(z.*ws.*I_r(month_temp_idx(i):month_temp_idx(i+1)) .* cos(sun_angle(month_temp_idx(i):month_temp_idx(i+1))).*A_wind_exposed);

    for j=1:length(Q_loss)-1
        E_loss_cond(i) = E_loss_cond(i)+ (Q_loss(j)+Q_loss(j+1))./2 .* timestep;
        E_sun(i) = E_sun(i) + (Q_sun(j)+Q_sun(j+1))./2 .* timestep;
    end

end

E_loss_cond  = E_loss_cond.*J2kwh ./100;
E_sun  = E_sun.*J2kwh ./100;
E_heat = -(E_loss_cond+E_sun);

figure;
hold on
plot(E_loss_cond)
plot(E_sun)
plot(E_heat)
legend('Loss', 'Sun', 'Heat');
hold off

