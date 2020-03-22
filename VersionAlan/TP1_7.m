%% Ejercicio 7
clc;
clear all;
close all;

% Lectura de datos
data = readtable('prueba.csv'); % Se lee el archivo CSV
t = table2array(data(:,1)); % Se obtiene un vector con los tiempos
val = table2array(data(:,2)); % Se obtiene un vector con los valores de la señal

% Cálculo de estadísticos
max = max(val)
min = min(val)
media = mean(val)

% Cálculo de fft
%f0 = 10; 
% Fs = 10*f0; 
% t = 0:1/Fs:1; 
val = sin(2*pi*f0*t);
val_fft = abs(fftshift(fft(val))); 
frec = 10*(-0.5:1/length(t):0.5-1/length(t));

% Gráficas
subplot(2,1,1);
plot(t,val)
title('Señal Senoidal (dominio temporal)')
xlabel('Tiempo')
ylabel('Amplitud')
 
subplot(2,1,2); 
plot(frec,val_fft)
title('Señal Senoidal (dominio frecuencial)')
xlabel('Frecuencia')
ylabel('Amplitud')

%prueba
% val_frec = fft(val);                               % Compute DFT of x
% m = abs(val_frec);                               % Magnitude
% y(m<1e-6) = 0;
% p = unwrap(angle(val_frec));                     % Phase
% f = (0:length(val_frec)-1)*100/length(val_frec);        % Frequency vector
%  
% subplot(3,1,2)
% plot(t,m)
% title('Magnitud')
% xlabel('Frecuencia')
% ylabel('Amplitud')
 
% subplot(3,1,3)
% plot(f,p*180/pi)
% title('Fase')
% xlabel('Frecuencia')
% ylabel('Amplitud')

% Guardado de datos
writetable(table(max, min, media), 'info.csv')
writetable(table(frec.', val_fft), 'fft.csv')
