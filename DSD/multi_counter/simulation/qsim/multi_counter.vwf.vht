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
-- Generated on "11/24/2023 19:27:35"
                                                             
-- Vhdl Test Bench(with test vectors) for design  :          multi_counter
-- 
-- Simulation tool : 3rd Party
-- 

LIBRARY ieee;                                               
USE ieee.std_logic_1164.all;                                

ENTITY multi_counter_vhd_vec_tst IS
END multi_counter_vhd_vec_tst;
ARCHITECTURE multi_counter_arch OF multi_counter_vhd_vec_tst IS
-- constants                                                 
-- signals                                                   
SIGNAL clk : STD_LOGIC;
SIGNAL clken : STD_LOGIC;
SIGNAL count : STD_LOGIC_VECTOR(3 DOWNTO 0);
SIGNAL cout : STD_LOGIC;
SIGNAL mode : STD_LOGIC_VECTOR(1 DOWNTO 0);
SIGNAL reset : STD_LOGIC;
COMPONENT multi_counter
	PORT (
	clk : IN STD_LOGIC;
	clken : IN STD_LOGIC;
	count : OUT STD_LOGIC_VECTOR(3 DOWNTO 0);
	cout : OUT STD_LOGIC;
	mode : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
	reset : IN STD_LOGIC
	);
END COMPONENT;
BEGIN
	i1 : multi_counter
	PORT MAP (
-- list connections between master ports and signals
	clk => clk,
	clken => clken,
	count => count,
	cout => cout,
	mode => mode,
	reset => reset
	);

-- reset
t_prcs_reset: PROCESS
BEGIN
	reset <= '0';
	WAIT FOR 50000 ps;
	reset <= '1';
WAIT;
END PROCESS t_prcs_reset;

-- clk
t_prcs_clk: PROCESS
BEGIN
	clk <= '1';
	WAIT FOR 5000 ps;
	FOR i IN 1 TO 99
	LOOP
		clk <= '0';
		WAIT FOR 5000 ps;
		clk <= '1';
		WAIT FOR 5000 ps;
	END LOOP;
	clk <= '0';
WAIT;
END PROCESS t_prcs_clk;

-- clken
t_prcs_clken: PROCESS
BEGIN
LOOP
	clken <= '0';
	WAIT FOR 30000 ps;
	clken <= '1';
	WAIT FOR 10000 ps;
	IF (NOW >= 1000000 ps) THEN WAIT; END IF;
END LOOP;
END PROCESS t_prcs_clken;
-- mode[1]
t_prcs_mode_1: PROCESS
BEGIN
	mode(1) <= '0';
	WAIT FOR 650000 ps;
	mode(1) <= '1';
WAIT;
END PROCESS t_prcs_mode_1;
-- mode[0]
t_prcs_mode_0: PROCESS
BEGIN
	mode(0) <= '0';
	WAIT FOR 410000 ps;
	mode(0) <= '1';
	WAIT FOR 240000 ps;
	mode(0) <= '0';
	WAIT FOR 150000 ps;
	mode(0) <= '1';
WAIT;
END PROCESS t_prcs_mode_0;
END multi_counter_arch;
