%Opgave 1.1

T=0.5; %Periode eller varighed

Ts = 0.0025; %Sample tid
fs=1/Ts; %Sample frekvens

N=T*fs; %antal samples same as:T/Ts

%Opgave 1.2

T=1; %Periode eller varighed

f0=350; %grund frekvens

fs1=1000; %Sample frekvens
fs2=4000;

N1=T*fs1; %antal samples same as:T/Ts
N2=T*fs2; %antal samples same as:T/Ts

t1 = [0:N1-1]/fs1;   % samme som [0:N1-1]*Ts1!
t2 = [0:N2-1]/fs2;   % samme som [0:N1-1]*Ts1!

s1_1 = sin(f0*2*pi*t1);
s2_1 = sin(f0*2*pi*t2);

stem(s1_1)


%Opgave 1.3

%definationer
f3=500; %frekvens
A=2.5; %amplitude
fase=deg2rad(120); %fase
offset=1; %DC offset
fs=4000;  %sample frekvens
T=1; %tiden



%udregninger

n=T*fs;
t=[0:n-1]/fs;

s3_1 = A*sin(f3*2*pi*t1+fase)+offset;
f1n=f3/fs;

%stem(s3_1);

%opgave  1.4
stem(t1,s1_1)
hold on
stem(t1,s3_1)
stem(t1,s1_1+s3_1)
hold off


