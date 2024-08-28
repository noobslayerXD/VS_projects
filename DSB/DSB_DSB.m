% Define parameters
fs = 22050; % Adjusted sampling frequency for faster playback
duration = 0.5; % Duration of each tone in seconds
fade_duration = 0.2; % Duration of the fade-out in seconds
amplitude = 1; % Amplitude of the tones

% Define frequencies for the tones representing "D", "S", and "B"
frequencies = [587.33, 987.77, 493.88]; % Frequencies for D, S, and B, respectively

% Generate time vector
t = 0:1/fs:duration;

% Generate tones for "D", "S", and "B" with fading out
tones = [];
for freq = frequencies
    tone = amplitude * sin(2*pi*freq*t) .* exp(-t/fade_duration);
    tones = [tones, tone];
end

% Play the jingle
soundsc(tones, fs);
