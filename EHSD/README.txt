GND/VCC bounce model - SN74ALVC244 on the DTU HW test board (LTspice)

Keep all files in the same folder:
  GND_VCC_bounce_QFN.asc   Q1, RGY package, IBIS component ALVC244_RGY
  GND_VCC_bounce_SOIC.asc  Q3, DW package,  IBIS component ALVC244_DW
  bounce_models.lib        DRV (controlled-resistor driver) and TL (T-line) subcircuits
  drv.asy, tl.asy          symbols for the two subcircuits
  reference_waveforms_ngspice.png  expected curves, for comparison

Running
  1. Open an .asc in LTspice and press Run. One run steps Nact = 1, 3, 7 active lines.
  2. MON=0 -> 8th line low -> GND bounce. Change the directive to MON=1 for VCC bounce.
  3. Useful traces:
       V(mon_scope)          8th line at the scope (channel 2, P39 QFN / P40 SOIC, 50 ohm)
       V(gnd_die), V(vcc_die) internal chip rails
       V(l1_rx) or V(l1_die) an active line, for timing reference
  4. Peak values per step: View > SPICE Error Log (.meas results).

Which line is which (from the board schematic)
  Row  Output  Pin  Toggles for   Source of input
  MON  2Y4     3    never         2A4: R34/J3 (QFN), R51/J6 (SOIC)
  L1   2Y3     5    1, 3, 7       2A3 <- F1 2Y2 (clock bank 2, J8)
  L2   1Y1     18   3, 7          1OE via J1/J4; input from clock bank 2
  L3   1Y2     16   3, 7          as L2
  L4   1Y3     14   7             1OE via J1/J4; input from clock bank 1 (J9)
  L5   1Y4     12   7             as L4
  L6   2Y1     9    7             2OE via J2/J5; input from clock bank 1 (J9)
  L7   2Y2     7    7             as L6
  Outputs that are enabled but whose clock bank is off are held low (CDCVF2310
  drives disabled outputs low); outputs with OE off are Hi-Z.

Values
  From IBIS: R_pin, L_pin, C_pin for VCC, GND and each output pin; Ccomp = 6.04 pF.
  From the assignment: Rdrv = 11 ohm, Rs = 39 ohm, T-line 50 ohm / 600 ps, 500 ps edges, 20 MHz.
  Estimates (tune to match measurements): Cdie = 20 pF on-die VCC-GND capacitance,
  Crx = 5 pF receiver, board supply R_brd/L_brd, decoupling ESL/ESR.
