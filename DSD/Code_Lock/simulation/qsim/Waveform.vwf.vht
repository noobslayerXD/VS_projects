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
-- Generated on "11/30/2023 19:09:44"
                                                             
-- Vhdl Test Bench(with test vectors) for design  :          code_lock_simple
-- 
-- Simulation tool : 3rd Party
-- 

LIBRARY ieee;                                               
USE ieee.std_logic_1164.all;                                

ENTITY code_lock_simple_vhd_vec_tst IS
END code_lock_simple_vhd_vec_tst;
ARCHITECTURE code_lock_simple_arch OF code_lock_simple_vhd_vec_tst IS
-- constants                                                 
-- signals                                                   
SIGNAL clk : STD_LOGIC;
SIGNAL code : STD_LOGIC_VECTOR(3 DOWNTO 0);
SIGNAL enter : STD_LOGIC;
SIGNAL err_count : STD_LOGIC_VECTOR(1 DOWNTO 0);
SIGNAL lock : STD_LOGIC;
SIGNAL lock0 : STD_LOGIC;
SIGNAL reset : STD_LOGIC;
COMPONENT code_lock_simple
	PORT (
	clk : IN STD_LOGIC;
	code : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
	enter : IN STD_LOGIC;
	err_count : OUT STD_LOGIC_VECTOR(1 DOWNTO 0);
	lock : OUT STD_LOGIC;
	lock0 : OUT STD_LOGIC;
	reset : IN STD_LOGIC
	);
END COMPONENT;
BEGIN
	i1 : code_lock_simple
	PORT MAP (
-- list connections between master ports and signals
	clk => clk,
	code => code,
	enter => enter,
	err_count => err_count,
	lock => lock,
	lock0 => lock0,
	reset => reset
	);

-- clk
t_prcs_clk: PROCESS
BEGIN
LOOP
	clk <= '0';
	WAIT FOR 10000 ps;
	clk <= '1';
	WAIT FOR 10000 ps;
	IF (NOW >= 1000000 ps) THEN WAIT; END IF;
END LOOP;
END PROCESS t_prcs_clk;
-- code[3]
t_prcs_code_3: PROCESS
BEGIN
	code(3) <= '0';
WAIT;
END PROCESS t_prcs_code_3;
-- code[2]
t_prcs_code_2: PROCESS
BEGIN
	code(2) <= '0';
	WAIT FOR 50000 ps;
	code(2) <= '1';
	WAIT FOR 20000 ps;
	code(2) <= '0';
WAIT;
END PROCESS t_prcs_code_2;
-- code[1]
t_prcs_code_1: PROCESS
BEGIN
	code(1) <= '0';
	WAIT FOR 10000 ps;
	code(1) <= '1';
	WAIT FOR 20000 ps;
	code(1) <= '0';
	WAIT FOR 20000 ps;
	code(1) <= '1';
	WAIT FOR 20000 ps;
	code(1) <= '0';
WAIT;
END PROCESS t_prcs_code_1;
-- code[0]
t_prcs_code_0: PROCESS
BEGIN
	code(0) <= '0';
	WAIT FOR 10000 ps;
	code(0) <= '1';
	WAIT FOR 20000 ps;
	code(0) <= '0';
	WAIT FOR 20000 ps;
	code(0) <= '1';
	WAIT FOR 20000 ps;
	code(0) <= '0';
WAIT;
END PROCESS t_prcs_code_0;

-- enter
t_prcs_enter: PROCESS
BEGIN
	enter <= '0';
	WAIT FOR 10000 ps;
	enter <= '1';
	WAIT FOR 20000 ps;
	enter <= '0';
	WAIT FOR 20000 ps;
	enter <= '1';
	WAIT FOR 20000 ps;
	enter <= '0';
WAIT;
END PROCESS t_prcs_enter;

-- reset
t_prcs_reset: PROCESS
BEGIN
	reset <= '0';
WAIT;
END PROCESS t_prcs_reset;
END code_lock_simple_arch;
