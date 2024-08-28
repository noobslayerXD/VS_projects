%% Opgave 1.5: Generer og afspil en sum af toner

% Definér samplefrekvensen
fs = 44100; % Hz

% Definér toner med forskellige frekvenser og amplituder
frequencies = [1000, 2000, 3000]; % Hz
amplitudes = [1, 0.5, 0.3];

% Generér de individuelle toner
t = 0:1/fs:1; % 1 sekunds signal
tones = zeros(size(t));
for i = 1:length(frequencies)
    tones = tones + amplitudes(i) * sin(2*pi*frequencies(i)*t);
end

% Afspil tonerne med den oprindelige samplefrekvens
soundsc(tones, fs);

% Afspil tonerne med en ny samplefrekvens (0.5 * fs)
new_fs = 0.5 * fs;
soundsc(tones, new_fs);

close(gcf); % Luk det aktive figurvindue

%% Opgave 1.6: Generer og plot to sinusoidale toner

% Difiner samplefrekvensen
f_sample = 6000; % Samplefrekvens i Hz

% Definér toner med deres frekvenser
f_1 = 2700; % Hz
f_2 = 3800; % Hz

% Generér et tidsvektor med passende længde
t = 0:1/f_sample:3; % F.eks. 3 sekunders signal

% Generér de to sinus toner
tone1 = sin(2*pi*f_1*t);
tone2 = sin(2*pi*f_2*t);

% Plot de to toner
figure;
subplot(2,1,1);
plot(t, tone1);
title('Tone 1: 2,7 kHz');
xlabel('Tid (s)');
ylabel('Amplitude');

subplot(2,1,2);
plot(t, tone2);
title('Tone 2: 3,8 kHz');
xlabel('Tid (s)');
ylabel('Amplitude');
grid on;

close(gcf); % Luk det aktive figurvindue

%% Opgave 1.7: Konstruer og plot et undersamplet signal

% Definer samplefrekvensen
fs = 6000; % Hz

% Definer tonerne med deres frekvenser
f1 = 2700; % Hz
f2 = 3800; % Hz

% Generér et tidsvektor med passende længde
t = 0:1/fs:0.1; % F.eks. 0.1 sekunders signal

% Generér de to toner
tone1 = sin(2*pi*f1*t);
tone2 = sin(2*pi*f2*t);

% Sammensæt de to toner
mixed_signal = tone1 + tone2;

% Nedsample signalet
downsample_factor = 3; % Faktor for nedsampling
undersampled_signal = downsample(mixed_signal, downsample_factor);

% Plot det originale og det undersamplede signal
figure;
subplot(2,1,1);
plot(t, mixed_signal);
title('Originalt signal');
xlabel('Tid (s)');
ylabel('Amplitude');
grid on;

subplot(2,1,2);
undersampled_t = 0:1/(fs/downsample_factor):0.1; % Ny tidsvektor efter nedsampling
plot(undersampled_t, undersampled_signal);
title('Undersamplet signal');
xlabel('Tid (s)');
ylabel('Amplitude');
grid on;

close(gcf); % Luk det aktive figurvindue

%% Opgave 1.9: Generer og plot eksponentielt aftagende toner

% Definer samplefrekvensen
fs = 6000; % Hz

% Definer tonerne med deres frekvenser
f1 = 2700; % Hz
f2 = 3800; % Hz

% Generér et tidsvektor med passende længde
t = 0:1/fs:3; % F.eks. 3 sekunders signal

% Eksperimentér med forskellige tidskonstanter
alpha_values = [0.1, 0.5, 1]; % Tidskonstanter

figure;
for i = 1:length(alpha_values)
    % Generer de eksponentielt aftagende toner
    tone1 = sin(2*pi*f1*t) .* exp(-alpha_values(i)*t);
    tone2 = sin(2*pi*f2*t) .* exp(-alpha_values(i)*t);
    
    % Plot de eksponentielt aftagende toner
    subplot(length(alpha_values), 1, i);
    plot(t, tone1);
    hold on;
    plot(t, tone2);
    hold off;
    title(['Tidskonstant: ', num2str(alpha_values(i))]);
    xlabel('Tid (s)');
    ylabel('Amplitude');
    legend('Tone 1', 'Tone 2');
    grid on;
end

close(gcf); % Luk det aktive figurvindue

%% Opgave 1.10: Konstruer og afspil et ekko-signal

% Definér ekko-længder
echo_lengths = [0.15, 0.04, 0.3]; % 150ms, 40ms, 300ms

% Definér ekko-forstærkningsfaktorer
echo_factors = [0.6, 0.8, 0.4];

% Vælg en af tonerne fra opgave 1.5
selected_tone = tones;

% Generér ekko-signaler med forskellige længder og forstærkningsfaktorer
echo_signals = zeros(length(echo_lengths), length(selected_tone));
for i = 1:length(echo_lengths)
    echo_length = round(echo_lengths(i) * fs);
    echo_signals(i, :) = [zeros(1, echo_length), echo_factors(i) * selected_tone(1:end-echo_length)];
end

% Afspil ekko-signalerne
for i = 1:length(echo_lengths)
    soundsc(echo_signals(i, :), fs);
    pause(2); % Vent i 2 sekunder mellem afspilninger
end

close(gcf); % Luk det aktive figurvindue
