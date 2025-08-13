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
-- Generated on "09/13/2023 11:11:20"
                                                             
-- Vhdl Test Bench(with test vectors) for design  :          four_bit_adder
-- 
-- Simulation tool : 3rd Party
-- 

LIBRARY ieee;                                               
USE ieee.std_logic_1164.all;                                

ENTITY four_bit_adder_vhd_vec_tst IS
END four_bit_adder_vhd_vec_tst;
ARCHITECTURE four_bit_adder_arch OF four_bit_adder_vhd_vec_tst IS
-- constants                                                 
-- signals                                                   
SIGNAL A : STD_LOGIC_VECTOR(3 DOWNTO 0);
SIGNAL B : STD_LOGIC_VECTOR(3 DOWNTO 0);
SIGNAL Cin : STD_LOGIC;
SIGNAL Cout : STD_LOGIC;
SIGNAL Sum : STD_LOGIC_VECTOR(3 DOWNTO 0);
COMPONENT four_bit_adder
	PORT (
	A : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
	B : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
	Cin : IN STD_LOGIC;
	Cout : OUT STD_LOGIC;
	Sum : OUT STD_LOGIC_VECTOR(3 DOWNTO 0)
	);
END COMPONENT;
BEGIN
	i1 : four_bit_adder
	PORT MAP (
-- list connections between master ports and signals
	A => A,
	B => B,
	Cin => Cin,
	Cout => Cout,
	Sum => Sum
	);
-- A[3]
t_prcs_A_3: PROCESS
BEGIN
	A(3) <= '0';
	WAIT FOR 120000 ps;
	A(3) <= '1';
	WAIT FOR 60000 ps;
	A(3) <= '0';
WAIT;
END PROCESS t_prcs_A_3;
-- A[2]
t_prcs_A_2: PROCESS
BEGIN
	A(2) <= '0';
	WAIT FOR 120000 ps;
	A(2) <= '1';
	WAIT FOR 60000 ps;
	A(2) <= '0';
WAIT;
END PROCESS t_prcs_A_2;
-- A[1]
t_prcs_A_1: PROCESS
BEGIN
	A(1) <= '0';
	WAIT FOR 120000 ps;
	A(1) <= '1';
	WAIT FOR 60000 ps;
	A(1) <= '0';
WAIT;
END PROCESS t_prcs_A_1;
-- A[0]
t_prcs_A_0: PROCESS
BEGIN
	A(0) <= '0';
	WAIT FOR 120000 ps;
	A(0) <= '1';
	WAIT FOR 60000 ps;
	A(0) <= '0';
WAIT;
END PROCESS t_prcs_A_0;
-- B[3]
t_prcs_B_3: PROCESS
BEGIN
	B(3) <= '0';
	WAIT FOR 120000 ps;
	B(3) <= '1';
	WAIT FOR 60000 ps;
	B(3) <= '0';
WAIT;
END PROCESS t_prcs_B_3;
-- B[2]
t_prcs_B_2: PROCESS
BEGIN
	B(2) <= '0';
	WAIT FOR 120000 ps;
	B(2) <= '1';
	WAIT FOR 60000 ps;
	B(2) <= '0';
WAIT;
END PROCESS t_prcs_B_2;
-- B[1]
t_prcs_B_1: PROCESS
BEGIN
	B(1) <= '0';
	WAIT FOR 120000 ps;
	B(1) <= '1';
	WAIT FOR 60000 ps;
	B(1) <= '0';
WAIT;
END PROCESS t_prcs_B_1;
-- B[0]
t_prcs_B_0: PROCESS
BEGIN
	B(0) <= '0';
	WAIT FOR 120000 ps;
	B(0) <= '1';
	WAIT FOR 60000 ps;
	B(0) <= '0';
WAIT;
END PROCESS t_prcs_B_0;

-- Cin
t_prcs_Cin: PROCESS
BEGIN
	Cin <= '0';
	WAIT FOR 160000 ps;
	Cin <= '1';
	WAIT FOR 30000 ps;
	Cin <= '0';
WAIT;
END PROCESS t_prcs_Cin;
END four_bit_adder_arch;
