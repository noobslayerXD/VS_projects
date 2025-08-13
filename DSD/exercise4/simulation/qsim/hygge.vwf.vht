-- Copyright (C) 2022  Intel Corporation. All rights reserved.
-- Your use of Intel Corporation's design tools, logic functions 
-- and other software and tools, and any partner logic 
-- functions, and any output files from any of the foregoing 
-- (including device programming or simulation files), and any 
-- associated documentation or information are expressly subject 
-- to the terms and conditions of the Intel Program License 
-- Subscription Agreement, the Intel Quartus Prime License Agreement,
-- the Intel FPGA IP License Agreement, or other applicable license
-- agreement, including, without limitation, that your use is for
-- the sole purpose of programming logic devices manufactured by
-- Intel and sold by Intel or its authorized distributors.  Please
-- refer to the applicable agreement for further details, at
-- https://fpgasoftware.intel.com/eula.

-- *****************************************************************************
-- This file contains a Vhdl test bench with test vectors .The test vectors     
-- are exported from a vector file in the Quartus Waveform Editor and apply to  
-- the top level entity of the current Quartus project .The user can use this   
-- testbench to simulate his design using a third-party simulation tool .       
-- *****************************************************************************
-- Generated on "10/25/2023 08:25:16"
                                                             
-- Vhdl Test Bench(with test vectors) for design  :          HexMux
-- 
-- Simulation tool : 3rd Party
-- 

LIBRARY ieee;                                               
USE ieee.std_logic_1164.all;                                

ENTITY HexMux_vhd_vec_tst IS
END HexMux_vhd_vec_tst;
ARCHITECTURE HexMux_arch OF HexMux_vhd_vec_tst IS
-- constants                                                 
-- signals                                                   
SIGNAL bin : STD_LOGIC_VECTOR(11 DOWNTO 0);
SIGNAL sel : STD_LOGIC_VECTOR(1 DOWNTO 0);
SIGNAL tsseg : STD_LOGIC_VECTOR(20 DOWNTO 0);
COMPONENT HexMux
	PORT (
	bin : IN STD_LOGIC_VECTOR(11 DOWNTO 0);
	sel : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
	tsseg : OUT STD_LOGIC_VECTOR(20 DOWNTO 0)
	);
END COMPONENT;
BEGIN
	i1 : HexMux
	PORT MAP (
-- list connections between master ports and signals
	bin => bin,
	sel => sel,
	tsseg => tsseg
	);
-- bin[11]
t_prcs_bin_11: PROCESS
BEGIN
	bin(11) <= '0';
	WAIT FOR 120000 ps;
	bin(11) <= '1';
	WAIT FOR 30000 ps;
	bin(11) <= '0';
WAIT;
END PROCESS t_prcs_bin_11;
-- bin[10]
t_prcs_bin_10: PROCESS
BEGIN
	bin(10) <= '0';
WAIT;
END PROCESS t_prcs_bin_10;
-- bin[9]
t_prcs_bin_9: PROCESS
BEGIN
	bin(9) <= '0';
	WAIT FOR 150000 ps;
	bin(9) <= '1';
	WAIT FOR 40000 ps;
	bin(9) <= '0';
WAIT;
END PROCESS t_prcs_bin_9;
-- bin[8]
t_prcs_bin_8: PROCESS
BEGIN
	bin(8) <= '0';
WAIT;
END PROCESS t_prcs_bin_8;
-- bin[7]
t_prcs_bin_7: PROCESS
BEGIN
	bin(7) <= '0';
WAIT;
END PROCESS t_prcs_bin_7;
-- bin[6]
t_prcs_bin_6: PROCESS
BEGIN
	bin(6) <= '0';
	WAIT FOR 150000 ps;
	bin(6) <= '1';
	WAIT FOR 10000 ps;
	bin(6) <= '0';
WAIT;
END PROCESS t_prcs_bin_6;
-- bin[5]
t_prcs_bin_5: PROCESS
BEGIN
	bin(5) <= '0';
WAIT;
END PROCESS t_prcs_bin_5;
-- bin[4]
t_prcs_bin_4: PROCESS
BEGIN
	bin(4) <= '0';
WAIT;
END PROCESS t_prcs_bin_4;
-- bin[3]
t_prcs_bin_3: PROCESS
BEGIN
	bin(3) <= '0';
	WAIT FOR 100000 ps;
	bin(3) <= '1';
	WAIT FOR 110000 ps;
	bin(3) <= '0';
WAIT;
END PROCESS t_prcs_bin_3;
-- bin[2]
t_prcs_bin_2: PROCESS
BEGIN
	bin(2) <= '0';
	WAIT FOR 100000 ps;
	bin(2) <= '1';
	WAIT FOR 110000 ps;
	bin(2) <= '0';
WAIT;
END PROCESS t_prcs_bin_2;
-- bin[1]
t_prcs_bin_1: PROCESS
BEGIN
	bin(1) <= '0';
WAIT;
END PROCESS t_prcs_bin_1;
-- bin[0]
t_prcs_bin_0: PROCESS
BEGIN
	bin(0) <= '0';
WAIT;
END PROCESS t_prcs_bin_0;
-- sel[1]
t_prcs_sel_1: PROCESS
BEGIN
	sel(1) <= '0';
	WAIT FOR 40000 ps;
	sel(1) <= '1';
	WAIT FOR 50000 ps;
	sel(1) <= '0';
WAIT;
END PROCESS t_prcs_sel_1;
-- sel[0]
t_prcs_sel_0: PROCESS
BEGIN
	sel(0) <= '0';
WAIT;
END PROCESS t_prcs_sel_0;
END HexMux_arch;
