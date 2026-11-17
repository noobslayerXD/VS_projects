Version 4
SymbolType CELL
LINE Normal 0 -96 0 -80
LINE Normal 0 -80 -12 -74
LINE Normal -12 -74 12 -62
LINE Normal 12 -62 -12 -50
LINE Normal -12 -50 12 -38
LINE Normal 12 -38 -12 -26
LINE Normal -12 -26 0 -20
LINE Normal 0 -20 0 20
LINE Normal 0 20 -12 26
LINE Normal -12 26 12 38
LINE Normal 12 38 -12 50
LINE Normal -12 50 12 62
LINE Normal 12 62 -12 74
LINE Normal -12 74 0 80
LINE Normal 0 80 0 96
LINE Normal 0 0 64 0
CIRCLE Normal -4 -4 4 4
LINE Normal -20 -28 20 -72
LINE Normal 20 -72 10 -70
LINE Normal 20 -72 18 -62
LINE Normal -20 72 20 28
LINE Normal 20 28 10 30
LINE Normal 20 28 18 38
LINE Normal -64 0 -40 0
LINE Normal -40 0 -40 -50
LINE Normal -40 -50 -10 -50
LINE Normal -40 0 -40 50
LINE Normal -40 50 -10 50
RECTANGLE Normal -52 -88 52 88
TEXT 22 -64 Left 1 Ru(IN)
TEXT 22 64 Left 1 Rd(IN)
WINDOW 0 -48 -176 Left 2
WINDOW 39 -48 -144 Left 1
SYMATTR Value DRV
SYMATTR Prefix X
SYMATTR SpiceLine EN=1 ACT=1 RON=11
SYMATTR Description Linear driver: pull-up/pull-down resistors controlled by IN (0..1)
PIN 0 -96 NONE 8
PINATTR PinName VCCD
PINATTR SpiceOrder 1
PIN 0 96 NONE 8
PINATTR PinName GNDD
PINATTR SpiceOrder 2
PIN -64 0 NONE 8
PINATTR PinName IN
PINATTR SpiceOrder 3
PIN 64 0 NONE 8
PINATTR PinName OUT
PINATTR SpiceOrder 4
