% Define parameters
fs = 44100; % Sampling frequency (Hz)
duration = 5; % Duration of the signal in seconds
start_frequency = 5000; % Starting frequency of the tone (Hz)
end_frequency = 100; % Ending frequency of the tone (Hz)
amplitude = 1; % Amplitude of the tone

% Generate time vector
t = 0:1/fs:duration;

% Calculate frequency decreasing over time (linear decrease)
frequency = linspace(start_frequency, end_frequency, length(t));

% Generate tone with decreasing frequency
tone = amplitude * sin(2*pi*frequency.*t);

% Play the sound
soundsc(tone, fs);
plot(tone)