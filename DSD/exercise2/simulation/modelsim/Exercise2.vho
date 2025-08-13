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

-- VENDOR "Altera"
-- PROGRAM "Quartus Prime"
-- VERSION "Version 21.1.1 Build 850 06/23/2022 SJ Lite Edition"

-- DATE "09/13/2023 11:02:30"

-- 
-- Device: Altera 10M50DAF484C7G Package FBGA484
-- 

-- 
-- This VHDL file should be used for Questa Intel FPGA (VHDL) only
-- 

LIBRARY FIFTYFIVENM;
LIBRARY IEEE;
USE FIFTYFIVENM.FIFTYFIVENM_COMPONENTS.ALL;
USE IEEE.STD_LOGIC_1164.ALL;

ENTITY 	my_xor_7 IS
    PORT (
	Cout : IN std_logic;
	f1 : OUT std_logic;
	A_3 : IN std_logic;
	B_3 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic
	);
END my_xor_7;

-- Design Ports Information


ARCHITECTURE structure OF my_xor_7 IS
SIGNAL gnd : std_logic := '0';
SIGNAL vcc : std_logic := '1';
SIGNAL unknown : std_logic := 'X';
SIGNAL ww_devoe : std_logic;
SIGNAL ww_devclrn : std_logic;
SIGNAL ww_devpor : std_logic;
SIGNAL ww_Cout : std_logic;
SIGNAL ww_f1 : std_logic;
SIGNAL ww_A_3 : std_logic;
SIGNAL ww_B_3 : std_logic;

BEGIN

ww_Cout <= Cout;
f1 <= ww_f1;
ww_A_3 <= A_3;
ww_B_3 <= B_3;
ww_devoe <= devoe;
ww_devclrn <= devclrn;
ww_devpor <= devpor;

-- Location: LCCOMB_X25_Y38_N28
f : fiftyfivenm_lcell_comb
-- Equation(s):
-- f1 = \B[3]~input_o\ $ (\A[3]~input_o\ $ (Cout1))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1010010101011010",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => ww_B_3,
	datac => ww_A_3,
	datad => ww_Cout,
	combout => ww_f1);
END structure;


LIBRARY FIFTYFIVENM;
LIBRARY IEEE;
USE FIFTYFIVENM.FIFTYFIVENM_COMPONENTS.ALL;
USE IEEE.STD_LOGIC_1164.ALL;

ENTITY 	half_adder_structural_7 IS
    PORT (
	Cout : IN std_logic;
	f : OUT std_logic;
	A_3 : IN std_logic;
	B_3 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic
	);
END half_adder_structural_7;

-- Design Ports Information


ARCHITECTURE structure OF half_adder_structural_7 IS
SIGNAL gnd : std_logic := '0';
SIGNAL vcc : std_logic := '1';
SIGNAL unknown : std_logic := 'X';
SIGNAL ww_devoe : std_logic;
SIGNAL ww_devclrn : std_logic;
SIGNAL ww_devpor : std_logic;
SIGNAL ww_Cout : std_logic;
SIGNAL ww_f : std_logic;
SIGNAL ww_A_3 : std_logic;
SIGNAL ww_B_3 : std_logic;

COMPONENT my_xor_7
    PORT (
	Cout : IN std_logic;
	f1 : OUT std_logic;
	A_3 : IN std_logic;
	B_3 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic);
END COMPONENT;

BEGIN

ww_Cout <= Cout;
f <= ww_f;
ww_A_3 <= A_3;
ww_B_3 <= B_3;
ww_devoe <= devoe;
ww_devclrn <= devclrn;
ww_devpor <= devpor;
u2 : my_xor_7
PORT MAP (
	Cout => ww_Cout,
	f1 => ww_f,
	A_3 => ww_A_3,
	B_3 => ww_B_3,
	devoe => ww_devoe,
	devclrn => ww_devclrn,
	devpor => ww_devpor);
END structure;


LIBRARY FIFTYFIVENM;
LIBRARY IEEE;
USE FIFTYFIVENM.FIFTYFIVENM_COMPONENTS.ALL;
USE IEEE.STD_LOGIC_1164.ALL;

ENTITY 	full_adder_3 IS
    PORT (
	Cout : IN std_logic;
	f : OUT std_logic;
	Cout1 : OUT std_logic;
	A_3 : IN std_logic;
	B_3 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic
	);
END full_adder_3;

-- Design Ports Information


ARCHITECTURE structure OF full_adder_3 IS
SIGNAL gnd : std_logic := '0';
SIGNAL vcc : std_logic := '1';
SIGNAL unknown : std_logic := 'X';
SIGNAL ww_devoe : std_logic;
SIGNAL ww_devclrn : std_logic;
SIGNAL ww_devpor : std_logic;
SIGNAL ww_Cout : std_logic;
SIGNAL ww_f : std_logic;
SIGNAL ww_Cout1 : std_logic;
SIGNAL ww_A_3 : std_logic;
SIGNAL ww_B_3 : std_logic;

COMPONENT half_adder_structural_7
    PORT (
	Cout : IN std_logic;
	f : OUT std_logic;
	A_3 : IN std_logic;
	B_3 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic);
END COMPONENT;

BEGIN

ww_Cout <= Cout;
f <= ww_f;
Cout1 <= ww_Cout1;
ww_A_3 <= A_3;
ww_B_3 <= B_3;
ww_devoe <= devoe;
ww_devclrn <= devclrn;
ww_devpor <= devpor;
h2 : half_adder_structural_7
PORT MAP (
	Cout => ww_Cout,
	f => ww_f,
	A_3 => ww_A_3,
	B_3 => ww_B_3,
	devoe => ww_devoe,
	devclrn => ww_devclrn,
	devpor => ww_devpor);

-- Location: LCCOMB_X25_Y38_N30
\Cout~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- Cout1 = (\B[3]~input_o\ & ((\A[3]~input_o\) # (Cout1))) # (!\B[3]~input_o\ & (\A[3]~input_o\ & Cout1))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111101010100000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => ww_B_3,
	datac => ww_A_3,
	datad => ww_Cout,
	combout => ww_Cout1);
END structure;


LIBRARY FIFTYFIVENM;
LIBRARY IEEE;
USE FIFTYFIVENM.FIFTYFIVENM_COMPONENTS.ALL;
USE IEEE.STD_LOGIC_1164.ALL;

ENTITY 	my_xor_5 IS
    PORT (
	Cout : IN std_logic;
	f1 : OUT std_logic;
	A_2 : IN std_logic;
	B_2 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic
	);
END my_xor_5;

-- Design Ports Information


ARCHITECTURE structure OF my_xor_5 IS
SIGNAL gnd : std_logic := '0';
SIGNAL vcc : std_logic := '1';
SIGNAL unknown : std_logic := 'X';
SIGNAL ww_devoe : std_logic;
SIGNAL ww_devclrn : std_logic;
SIGNAL ww_devpor : std_logic;
SIGNAL ww_Cout : std_logic;
SIGNAL ww_f1 : std_logic;
SIGNAL ww_A_2 : std_logic;
SIGNAL ww_B_2 : std_logic;

BEGIN

ww_Cout <= Cout;
f1 <= ww_f1;
ww_A_2 <= A_2;
ww_B_2 <= B_2;
ww_devoe <= devoe;
ww_devclrn <= devclrn;
ww_devpor <= devpor;

-- Location: LCCOMB_X25_Y38_N0
f : fiftyfivenm_lcell_comb
-- Equation(s):
-- f1 = \B[2]~input_o\ $ (\A[2]~input_o\ $ (Cout1))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1010010101011010",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => ww_B_2,
	datac => ww_A_2,
	datad => ww_Cout,
	combout => ww_f1);
END structure;


LIBRARY FIFTYFIVENM;
LIBRARY IEEE;
USE FIFTYFIVENM.FIFTYFIVENM_COMPONENTS.ALL;
USE IEEE.STD_LOGIC_1164.ALL;

ENTITY 	half_adder_structural_5 IS
    PORT (
	Cout : IN std_logic;
	f : OUT std_logic;
	A_2 : IN std_logic;
	B_2 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic
	);
END half_adder_structural_5;

-- Design Ports Information


ARCHITECTURE structure OF half_adder_structural_5 IS
SIGNAL gnd : std_logic := '0';
SIGNAL vcc : std_logic := '1';
SIGNAL unknown : std_logic := 'X';
SIGNAL ww_devoe : std_logic;
SIGNAL ww_devclrn : std_logic;
SIGNAL ww_devpor : std_logic;
SIGNAL ww_Cout : std_logic;
SIGNAL ww_f : std_logic;
SIGNAL ww_A_2 : std_logic;
SIGNAL ww_B_2 : std_logic;

COMPONENT my_xor_5
    PORT (
	Cout : IN std_logic;
	f1 : OUT std_logic;
	A_2 : IN std_logic;
	B_2 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic);
END COMPONENT;

BEGIN

ww_Cout <= Cout;
f <= ww_f;
ww_A_2 <= A_2;
ww_B_2 <= B_2;
ww_devoe <= devoe;
ww_devclrn <= devclrn;
ww_devpor <= devpor;
u2 : my_xor_5
PORT MAP (
	Cout => ww_Cout,
	f1 => ww_f,
	A_2 => ww_A_2,
	B_2 => ww_B_2,
	devoe => ww_devoe,
	devclrn => ww_devclrn,
	devpor => ww_devpor);
END structure;


LIBRARY FIFTYFIVENM;
LIBRARY IEEE;
USE FIFTYFIVENM.FIFTYFIVENM_COMPONENTS.ALL;
USE IEEE.STD_LOGIC_1164.ALL;

ENTITY 	full_adder_2 IS
    PORT (
	Cout : IN std_logic;
	f : OUT std_logic;
	Cout1 : OUT std_logic;
	A_2 : IN std_logic;
	B_2 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic
	);
END full_adder_2;

-- Design Ports Information


ARCHITECTURE structure OF full_adder_2 IS
SIGNAL gnd : std_logic := '0';
SIGNAL vcc : std_logic := '1';
SIGNAL unknown : std_logic := 'X';
SIGNAL ww_devoe : std_logic;
SIGNAL ww_devclrn : std_logic;
SIGNAL ww_devpor : std_logic;
SIGNAL ww_Cout : std_logic;
SIGNAL ww_f : std_logic;
SIGNAL ww_Cout1 : std_logic;
SIGNAL ww_A_2 : std_logic;
SIGNAL ww_B_2 : std_logic;

COMPONENT half_adder_structural_5
    PORT (
	Cout : IN std_logic;
	f : OUT std_logic;
	A_2 : IN std_logic;
	B_2 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic);
END COMPONENT;

BEGIN

ww_Cout <= Cout;
f <= ww_f;
Cout1 <= ww_Cout1;
ww_A_2 <= A_2;
ww_B_2 <= B_2;
ww_devoe <= devoe;
ww_devclrn <= devclrn;
ww_devpor <= devpor;
h2 : half_adder_structural_5
PORT MAP (
	Cout => ww_Cout,
	f => ww_f,
	A_2 => ww_A_2,
	B_2 => ww_B_2,
	devoe => ww_devoe,
	devclrn => ww_devclrn,
	devpor => ww_devpor);

-- Location: LCCOMB_X25_Y38_N10
\Cout~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- Cout1 = (\B[2]~input_o\ & ((\A[2]~input_o\) # (Cout1))) # (!\B[2]~input_o\ & (\A[2]~input_o\ & Cout1))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111101010100000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => ww_B_2,
	datac => ww_A_2,
	datad => ww_Cout,
	combout => ww_Cout1);
END structure;


LIBRARY FIFTYFIVENM;
LIBRARY IEEE;
USE FIFTYFIVENM.FIFTYFIVENM_COMPONENTS.ALL;
USE IEEE.STD_LOGIC_1164.ALL;

ENTITY 	my_xor_3 IS
    PORT (
	Cout : IN std_logic;
	f1 : OUT std_logic;
	B_1 : IN std_logic;
	A_1 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic
	);
END my_xor_3;

-- Design Ports Information


ARCHITECTURE structure OF my_xor_3 IS
SIGNAL gnd : std_logic := '0';
SIGNAL vcc : std_logic := '1';
SIGNAL unknown : std_logic := 'X';
SIGNAL ww_devoe : std_logic;
SIGNAL ww_devclrn : std_logic;
SIGNAL ww_devpor : std_logic;
SIGNAL ww_Cout : std_logic;
SIGNAL ww_f1 : std_logic;
SIGNAL ww_B_1 : std_logic;
SIGNAL ww_A_1 : std_logic;

BEGIN

ww_Cout <= Cout;
f1 <= ww_f1;
ww_B_1 <= B_1;
ww_A_1 <= A_1;
ww_devoe <= devoe;
ww_devclrn <= devclrn;
ww_devpor <= devpor;

-- Location: LCCOMB_X25_Y38_N4
f : fiftyfivenm_lcell_comb
-- Equation(s):
-- f1 = \A[1]~input_o\ $ (Cout $ (\B[1]~input_o\))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1100001100111100",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datab => ww_A_1,
	datac => ww_Cout,
	datad => ww_B_1,
	combout => ww_f1);
END structure;


LIBRARY FIFTYFIVENM;
LIBRARY IEEE;
USE FIFTYFIVENM.FIFTYFIVENM_COMPONENTS.ALL;
USE IEEE.STD_LOGIC_1164.ALL;

ENTITY 	half_adder_structural_3 IS
    PORT (
	Cout : IN std_logic;
	f : OUT std_logic;
	B_1 : IN std_logic;
	A_1 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic
	);
END half_adder_structural_3;

-- Design Ports Information


ARCHITECTURE structure OF half_adder_structural_3 IS
SIGNAL gnd : std_logic := '0';
SIGNAL vcc : std_logic := '1';
SIGNAL unknown : std_logic := 'X';
SIGNAL ww_devoe : std_logic;
SIGNAL ww_devclrn : std_logic;
SIGNAL ww_devpor : std_logic;
SIGNAL ww_Cout : std_logic;
SIGNAL ww_f : std_logic;
SIGNAL ww_B_1 : std_logic;
SIGNAL ww_A_1 : std_logic;

COMPONENT my_xor_3
    PORT (
	Cout : IN std_logic;
	f1 : OUT std_logic;
	B_1 : IN std_logic;
	A_1 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic);
END COMPONENT;

BEGIN

ww_Cout <= Cout;
f <= ww_f;
ww_B_1 <= B_1;
ww_A_1 <= A_1;
ww_devoe <= devoe;
ww_devclrn <= devclrn;
ww_devpor <= devpor;
u2 : my_xor_3
PORT MAP (
	Cout => ww_Cout,
	f1 => ww_f,
	B_1 => ww_B_1,
	A_1 => ww_A_1,
	devoe => ww_devoe,
	devclrn => ww_devclrn,
	devpor => ww_devpor);
END structure;


LIBRARY FIFTYFIVENM;
LIBRARY IEEE;
USE FIFTYFIVENM.FIFTYFIVENM_COMPONENTS.ALL;
USE IEEE.STD_LOGIC_1164.ALL;

ENTITY 	full_adder_1 IS
    PORT (
	Cout : IN std_logic;
	f : OUT std_logic;
	Cout1 : OUT std_logic;
	B_1 : IN std_logic;
	A_1 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic
	);
END full_adder_1;

-- Design Ports Information


ARCHITECTURE structure OF full_adder_1 IS
SIGNAL gnd : std_logic := '0';
SIGNAL vcc : std_logic := '1';
SIGNAL unknown : std_logic := 'X';
SIGNAL ww_devoe : std_logic;
SIGNAL ww_devclrn : std_logic;
SIGNAL ww_devpor : std_logic;
SIGNAL ww_Cout : std_logic;
SIGNAL ww_f : std_logic;
SIGNAL ww_Cout1 : std_logic;
SIGNAL ww_B_1 : std_logic;
SIGNAL ww_A_1 : std_logic;

COMPONENT half_adder_structural_3
    PORT (
	Cout : IN std_logic;
	f : OUT std_logic;
	B_1 : IN std_logic;
	A_1 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic);
END COMPONENT;

BEGIN

ww_Cout <= Cout;
f <= ww_f;
Cout1 <= ww_Cout1;
ww_B_1 <= B_1;
ww_A_1 <= A_1;
ww_devoe <= devoe;
ww_devclrn <= devclrn;
ww_devpor <= devpor;
h2 : half_adder_structural_3
PORT MAP (
	Cout => ww_Cout,
	f => ww_f,
	B_1 => ww_B_1,
	A_1 => ww_A_1,
	devoe => ww_devoe,
	devclrn => ww_devclrn,
	devpor => ww_devpor);

-- Location: LCCOMB_X25_Y38_N6
\Cout~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- Cout1 = (\A[1]~input_o\ & ((Cout) # (\B[1]~input_o\))) # (!\A[1]~input_o\ & (Cout & \B[1]~input_o\))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111110011000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datab => ww_A_1,
	datac => ww_Cout,
	datad => ww_B_1,
	combout => ww_Cout1);
END structure;


LIBRARY FIFTYFIVENM;
LIBRARY IEEE;
USE FIFTYFIVENM.FIFTYFIVENM_COMPONENTS.ALL;
USE IEEE.STD_LOGIC_1164.ALL;

ENTITY 	my_xor_1 IS
    PORT (
	f : OUT std_logic;
	Cin : IN std_logic;
	A_0 : IN std_logic;
	B_0 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic
	);
END my_xor_1;

-- Design Ports Information


ARCHITECTURE structure OF my_xor_1 IS
SIGNAL gnd : std_logic := '0';
SIGNAL vcc : std_logic := '1';
SIGNAL unknown : std_logic := 'X';
SIGNAL ww_devoe : std_logic;
SIGNAL ww_devclrn : std_logic;
SIGNAL ww_devpor : std_logic;
SIGNAL ww_f : std_logic;
SIGNAL ww_Cin : std_logic;
SIGNAL ww_A_0 : std_logic;
SIGNAL ww_B_0 : std_logic;

BEGIN

f <= ww_f;
ww_Cin <= Cin;
ww_A_0 <= A_0;
ww_B_0 <= B_0;
ww_devoe <= devoe;
ww_devclrn <= devclrn;
ww_devpor <= devpor;

-- Location: LCCOMB_X25_Y38_N24
\f~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- f = \B[0]~input_o\ $ (\A[0]~input_o\ $ (\Cin~input_o\))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1001011010010110",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => ww_B_0,
	datab => ww_A_0,
	datac => ww_Cin,
	combout => ww_f);
END structure;


LIBRARY FIFTYFIVENM;
LIBRARY IEEE;
USE FIFTYFIVENM.FIFTYFIVENM_COMPONENTS.ALL;
USE IEEE.STD_LOGIC_1164.ALL;

ENTITY 	half_adder_structural_1 IS
    PORT (
	Sum : OUT std_logic;
	Cin : IN std_logic;
	A_0 : IN std_logic;
	B_0 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic
	);
END half_adder_structural_1;

-- Design Ports Information


ARCHITECTURE structure OF half_adder_structural_1 IS
SIGNAL gnd : std_logic := '0';
SIGNAL vcc : std_logic := '1';
SIGNAL unknown : std_logic := 'X';
SIGNAL ww_devoe : std_logic;
SIGNAL ww_devclrn : std_logic;
SIGNAL ww_devpor : std_logic;
SIGNAL ww_Sum : std_logic;
SIGNAL ww_Cin : std_logic;
SIGNAL ww_A_0 : std_logic;
SIGNAL ww_B_0 : std_logic;

COMPONENT my_xor_1
    PORT (
	f : OUT std_logic;
	Cin : IN std_logic;
	A_0 : IN std_logic;
	B_0 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic);
END COMPONENT;

BEGIN

Sum <= ww_Sum;
ww_Cin <= Cin;
ww_A_0 <= A_0;
ww_B_0 <= B_0;
ww_devoe <= devoe;
ww_devclrn <= devclrn;
ww_devpor <= devpor;
u2 : my_xor_1
PORT MAP (
	f => ww_Sum,
	Cin => ww_Cin,
	A_0 => ww_A_0,
	B_0 => ww_B_0,
	devoe => ww_devoe,
	devclrn => ww_devclrn,
	devpor => ww_devpor);
END structure;


LIBRARY FIFTYFIVENM;
LIBRARY IEEE;
USE FIFTYFIVENM.FIFTYFIVENM_COMPONENTS.ALL;
USE IEEE.STD_LOGIC_1164.ALL;

ENTITY 	full_adder IS
    PORT (
	Sum : OUT std_logic;
	Cout : OUT std_logic;
	Cin : IN std_logic;
	A_0 : IN std_logic;
	B_0 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic
	);
END full_adder;

-- Design Ports Information


ARCHITECTURE structure OF full_adder IS
SIGNAL gnd : std_logic := '0';
SIGNAL vcc : std_logic := '1';
SIGNAL unknown : std_logic := 'X';
SIGNAL ww_devoe : std_logic;
SIGNAL ww_devclrn : std_logic;
SIGNAL ww_devpor : std_logic;
SIGNAL ww_Sum : std_logic;
SIGNAL ww_Cout : std_logic;
SIGNAL ww_Cin : std_logic;
SIGNAL ww_A_0 : std_logic;
SIGNAL ww_B_0 : std_logic;

COMPONENT half_adder_structural_1
    PORT (
	Sum : OUT std_logic;
	Cin : IN std_logic;
	A_0 : IN std_logic;
	B_0 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic);
END COMPONENT;

BEGIN

Sum <= ww_Sum;
Cout <= ww_Cout;
ww_Cin <= Cin;
ww_A_0 <= A_0;
ww_B_0 <= B_0;
ww_devoe <= devoe;
ww_devclrn <= devclrn;
ww_devpor <= devpor;
h2 : half_adder_structural_1
PORT MAP (
	Sum => ww_Sum,
	Cin => ww_Cin,
	A_0 => ww_A_0,
	B_0 => ww_B_0,
	devoe => ww_devoe,
	devclrn => ww_devclrn,
	devpor => ww_devpor);

-- Location: LCCOMB_X25_Y38_N26
\Cout~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- Cout = (\B[0]~input_o\ & ((\A[0]~input_o\) # (\Cin~input_o\))) # (!\B[0]~input_o\ & (\A[0]~input_o\ & \Cin~input_o\))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1110100011101000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => ww_B_0,
	datab => ww_A_0,
	datac => ww_Cin,
	combout => ww_Cout);
END structure;


LIBRARY FIFTYFIVENM;
LIBRARY IEEE;
USE FIFTYFIVENM.FIFTYFIVENM_COMPONENTS.ALL;
USE IEEE.STD_LOGIC_1164.ALL;

ENTITY 	four_bit_adder IS
    PORT (
	Cin : IN std_logic;
	A : IN std_logic_vector(3 DOWNTO 0);
	B : IN std_logic_vector(3 DOWNTO 0);
	Sum : OUT std_logic_vector(3 DOWNTO 0);
	Cout : OUT std_logic
	);
END four_bit_adder;

-- Design Ports Information
-- Sum[0]	=>  Location: PIN_C4,	 I/O Standard: 3.3-V LVTTL,	 Current Strength: 8mA
-- Sum[1]	=>  Location: PIN_C3,	 I/O Standard: 3.3-V LVTTL,	 Current Strength: 8mA
-- Sum[2]	=>  Location: PIN_B4,	 I/O Standard: 3.3-V LVTTL,	 Current Strength: 8mA
-- Sum[3]	=>  Location: PIN_F7,	 I/O Standard: 3.3-V LVTTL,	 Current Strength: 8mA
-- Cout	=>  Location: PIN_E8,	 I/O Standard: 3.3-V LVTTL,	 Current Strength: 8mA
-- Cin	=>  Location: PIN_A3,	 I/O Standard: 3.3-V LVTTL,	 Current Strength: Default
-- A[0]	=>  Location: PIN_B1,	 I/O Standard: 3.3-V LVTTL,	 Current Strength: Default
-- B[0]	=>  Location: PIN_B2,	 I/O Standard: 3.3-V LVTTL,	 Current Strength: Default
-- B[1]	=>  Location: PIN_B5,	 I/O Standard: 3.3-V LVTTL,	 Current Strength: Default
-- A[1]	=>  Location: PIN_B3,	 I/O Standard: 3.3-V LVTTL,	 Current Strength: Default
-- A[2]	=>  Location: PIN_C5,	 I/O Standard: 3.3-V LVTTL,	 Current Strength: Default
-- B[2]	=>  Location: PIN_D6,	 I/O Standard: 3.3-V LVTTL,	 Current Strength: Default
-- A[3]	=>  Location: PIN_A2,	 I/O Standard: 3.3-V LVTTL,	 Current Strength: Default
-- B[3]	=>  Location: PIN_D5,	 I/O Standard: 3.3-V LVTTL,	 Current Strength: Default


ARCHITECTURE structure OF four_bit_adder IS
SIGNAL gnd : std_logic := '0';
SIGNAL vcc : std_logic := '1';
SIGNAL unknown : std_logic := 'X';
SIGNAL devoe : std_logic := '1';
SIGNAL devclrn : std_logic := '1';
SIGNAL devpor : std_logic := '1';
SIGNAL ww_devoe : std_logic;
SIGNAL ww_devclrn : std_logic;
SIGNAL ww_devpor : std_logic;
SIGNAL ww_Cin : std_logic;
SIGNAL ww_A : std_logic_vector(3 DOWNTO 0);
SIGNAL ww_B : std_logic_vector(3 DOWNTO 0);
SIGNAL ww_Sum : std_logic_vector(3 DOWNTO 0);
SIGNAL ww_Cout : std_logic;
SIGNAL \~QUARTUS_CREATED_ADC1~_CHSEL_bus\ : std_logic_vector(4 DOWNTO 0);
SIGNAL \~QUARTUS_CREATED_ADC2~_CHSEL_bus\ : std_logic_vector(4 DOWNTO 0);
SIGNAL \fa1|h2|u2|f~0_combout\ : std_logic;
SIGNAL \fa1|Cout~0_combout\ : std_logic;
SIGNAL \fa2|h2|u2|f~combout\ : std_logic;
SIGNAL \fa2|Cout~0_combout\ : std_logic;
SIGNAL \fa3|h2|u2|f~combout\ : std_logic;
SIGNAL \fa3|Cout~0_combout\ : std_logic;
SIGNAL \fa4|h2|u2|f~combout\ : std_logic;
SIGNAL \fa4|Cout~0_combout\ : std_logic;
SIGNAL \Cin~input_o\ : std_logic;
SIGNAL \A[0]~input_o\ : std_logic;
SIGNAL \B[0]~input_o\ : std_logic;
SIGNAL \B[1]~input_o\ : std_logic;
SIGNAL \A[1]~input_o\ : std_logic;
SIGNAL \A[2]~input_o\ : std_logic;
SIGNAL \B[2]~input_o\ : std_logic;
SIGNAL \A[3]~input_o\ : std_logic;
SIGNAL \B[3]~input_o\ : std_logic;
SIGNAL \~QUARTUS_CREATED_GND~I_combout\ : std_logic;
SIGNAL \~QUARTUS_CREATED_UNVM~~busy\ : std_logic;
SIGNAL \~ALTERA_TMS~~ibuf_o\ : std_logic;
SIGNAL \~ALTERA_TMS~~padout\ : std_logic;
SIGNAL \~ALTERA_TCK~~ibuf_o\ : std_logic;
SIGNAL \~ALTERA_TCK~~padout\ : std_logic;
SIGNAL \~ALTERA_TDI~~ibuf_o\ : std_logic;
SIGNAL \~ALTERA_TDI~~padout\ : std_logic;
SIGNAL \~ALTERA_TDO~~padout\ : std_logic;
SIGNAL \~ALTERA_CONFIG_SEL~~ibuf_o\ : std_logic;
SIGNAL \~ALTERA_CONFIG_SEL~~padout\ : std_logic;
SIGNAL \~ALTERA_nCONFIG~~ibuf_o\ : std_logic;
SIGNAL \~ALTERA_nCONFIG~~padout\ : std_logic;
SIGNAL \~ALTERA_nSTATUS~~ibuf_o\ : std_logic;
SIGNAL \~ALTERA_nSTATUS~~padout\ : std_logic;
SIGNAL \~ALTERA_CONF_DONE~~ibuf_o\ : std_logic;
SIGNAL \~ALTERA_CONF_DONE~~padout\ : std_logic;
SIGNAL \~QUARTUS_CREATED_ADC1~~eoc\ : std_logic;
SIGNAL \~QUARTUS_CREATED_ADC2~~eoc\ : std_logic;
SIGNAL \~ALTERA_TDO~~obuf_o\ : std_logic;

COMPONENT full_adder_3
    PORT (
	Cout : IN std_logic;
	f : OUT std_logic;
	Cout1 : OUT std_logic;
	A_3 : IN std_logic;
	B_3 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic);
END COMPONENT;

COMPONENT full_adder_2
    PORT (
	Cout : IN std_logic;
	f : OUT std_logic;
	Cout1 : OUT std_logic;
	A_2 : IN std_logic;
	B_2 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic);
END COMPONENT;

COMPONENT full_adder_1
    PORT (
	Cout : IN std_logic;
	f : OUT std_logic;
	Cout1 : OUT std_logic;
	B_1 : IN std_logic;
	A_1 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic);
END COMPONENT;

COMPONENT full_adder
    PORT (
	Sum : OUT std_logic;
	Cout : OUT std_logic;
	Cin : IN std_logic;
	A_0 : IN std_logic;
	B_0 : IN std_logic;
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic);
END COMPONENT;

BEGIN

ww_Cin <= Cin;
ww_A <= A;
ww_B <= B;
Sum <= ww_Sum;
Cout <= ww_Cout;
ww_devoe <= devoe;
ww_devclrn <= devclrn;
ww_devpor <= devpor;

\~QUARTUS_CREATED_ADC1~_CHSEL_bus\ <= (\~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\);

\~QUARTUS_CREATED_ADC2~_CHSEL_bus\ <= (\~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\);
fa4 : full_adder_3
PORT MAP (
	Cout => \fa3|Cout~0_combout\,
	f => \fa4|h2|u2|f~combout\,
	Cout1 => \fa4|Cout~0_combout\,
	A_3 => \A[3]~input_o\,
	B_3 => \B[3]~input_o\,
	devoe => ww_devoe,
	devclrn => ww_devclrn,
	devpor => ww_devpor);
fa3 : full_adder_2
PORT MAP (
	Cout => \fa2|Cout~0_combout\,
	f => \fa3|h2|u2|f~combout\,
	Cout1 => \fa3|Cout~0_combout\,
	A_2 => \A[2]~input_o\,
	B_2 => \B[2]~input_o\,
	devoe => ww_devoe,
	devclrn => ww_devclrn,
	devpor => ww_devpor);
fa2 : full_adder_1
PORT MAP (
	Cout => \fa1|Cout~0_combout\,
	f => \fa2|h2|u2|f~combout\,
	Cout1 => \fa2|Cout~0_combout\,
	B_1 => \B[1]~input_o\,
	A_1 => \A[1]~input_o\,
	devoe => ww_devoe,
	devclrn => ww_devclrn,
	devpor => ww_devpor);
fa1 : full_adder
PORT MAP (
	Sum => \fa1|h2|u2|f~0_combout\,
	Cout => \fa1|Cout~0_combout\,
	Cin => \Cin~input_o\,
	A_0 => \A[0]~input_o\,
	B_0 => \B[0]~input_o\,
	devoe => ww_devoe,
	devclrn => ww_devclrn,
	devpor => ww_devpor);

-- Location: IOIBUF_X26_Y39_N8
\Cin~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_Cin,
	o => \Cin~input_o\);

-- Location: IOIBUF_X22_Y39_N22
\A[0]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_A(0),
	o => \A[0]~input_o\);

-- Location: IOIBUF_X22_Y39_N15
\B[0]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_B(0),
	o => \B[0]~input_o\);

-- Location: IOIBUF_X26_Y39_N29
\B[1]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_B(1),
	o => \B[1]~input_o\);

-- Location: IOIBUF_X26_Y39_N15
\A[1]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_A(1),
	o => \A[1]~input_o\);

-- Location: IOIBUF_X24_Y39_N22
\A[2]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_A(2),
	o => \A[2]~input_o\);

-- Location: IOIBUF_X22_Y39_N29
\B[2]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_B(2),
	o => \B[2]~input_o\);

-- Location: IOIBUF_X26_Y39_N1
\A[3]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_A(3),
	o => \A[3]~input_o\);

-- Location: IOIBUF_X24_Y39_N29
\B[3]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_B(3),
	o => \B[3]~input_o\);

-- Location: LCCOMB_X44_Y41_N8
\~QUARTUS_CREATED_GND~I\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \~QUARTUS_CREATED_GND~I_combout\ = GND

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0000000000000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	combout => \~QUARTUS_CREATED_GND~I_combout\);

-- Location: IOOBUF_X24_Y39_N2
\Sum[0]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \fa1|h2|u2|f~0_combout\,
	devoe => ww_devoe,
	o => ww_Sum(0));

-- Location: IOOBUF_X20_Y39_N9
\Sum[1]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \fa2|h2|u2|f~combout\,
	devoe => ww_devoe,
	o => ww_Sum(1));

-- Location: IOOBUF_X26_Y39_N23
\Sum[2]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \fa3|h2|u2|f~combout\,
	devoe => ww_devoe,
	o => ww_Sum(2));

-- Location: IOOBUF_X24_Y39_N16
\Sum[3]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \fa4|h2|u2|f~combout\,
	devoe => ww_devoe,
	o => ww_Sum(3));

-- Location: IOOBUF_X24_Y39_N9
\Cout~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \fa4|Cout~0_combout\,
	devoe => ww_devoe,
	o => ww_Cout);

-- Location: UNVM_X0_Y40_N40
\~QUARTUS_CREATED_UNVM~\ : fiftyfivenm_unvm
-- pragma translate_off
GENERIC MAP (
	addr_range1_end_addr => -1,
	addr_range1_offset => -1,
	addr_range2_end_addr => -1,
	addr_range2_offset => -1,
	addr_range3_offset => -1,
	is_compressed_image => "false",
	is_dual_boot => "false",
	is_eram_skip => "false",
	max_ufm_valid_addr => -1,
	max_valid_addr => -1,
	min_ufm_valid_addr => -1,
	min_valid_addr => -1,
	part_name => "quartus_created_unvm",
	reserve_block => "true")
-- pragma translate_on
PORT MAP (
	nosc_ena => \~QUARTUS_CREATED_GND~I_combout\,
	xe_ye => \~QUARTUS_CREATED_GND~I_combout\,
	se => \~QUARTUS_CREATED_GND~I_combout\,
	busy => \~QUARTUS_CREATED_UNVM~~busy\);

-- Location: ADCBLOCK_X43_Y52_N0
\~QUARTUS_CREATED_ADC1~\ : fiftyfivenm_adcblock
-- pragma translate_off
GENERIC MAP (
	analog_input_pin_mask => 0,
	clkdiv => 1,
	device_partname_fivechar_prefix => "none",
	is_this_first_or_second_adc => 1,
	prescalar => 0,
	pwd => 1,
	refsel => 0,
	reserve_block => "true",
	testbits => 66,
	tsclkdiv => 1,
	tsclksel => 0)
-- pragma translate_on
PORT MAP (
	soc => \~QUARTUS_CREATED_GND~I_combout\,
	usr_pwd => VCC,
	tsen => \~QUARTUS_CREATED_GND~I_combout\,
	chsel => \~QUARTUS_CREATED_ADC1~_CHSEL_bus\,
	eoc => \~QUARTUS_CREATED_ADC1~~eoc\);

-- Location: ADCBLOCK_X43_Y51_N0
\~QUARTUS_CREATED_ADC2~\ : fiftyfivenm_adcblock
-- pragma translate_off
GENERIC MAP (
	analog_input_pin_mask => 0,
	clkdiv => 1,
	device_partname_fivechar_prefix => "none",
	is_this_first_or_second_adc => 2,
	prescalar => 0,
	pwd => 1,
	refsel => 0,
	reserve_block => "true",
	testbits => 66,
	tsclkdiv => 1,
	tsclksel => 0)
-- pragma translate_on
PORT MAP (
	soc => \~QUARTUS_CREATED_GND~I_combout\,
	usr_pwd => VCC,
	tsen => \~QUARTUS_CREATED_GND~I_combout\,
	chsel => \~QUARTUS_CREATED_ADC2~_CHSEL_bus\,
	eoc => \~QUARTUS_CREATED_ADC2~~eoc\);
END structure;


