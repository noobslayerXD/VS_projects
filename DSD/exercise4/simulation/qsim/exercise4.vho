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

-- DATE "10/25/2023 08:25:17"

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

ENTITY 	hard_block IS
    PORT (
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic
	);
END hard_block;

-- Design Ports Information
-- ~ALTERA_TMS~	=>  Location: PIN_H2,	 I/O Standard: 2.5 V Schmitt Trigger,	 Current Strength: Default
-- ~ALTERA_TCK~	=>  Location: PIN_G2,	 I/O Standard: 2.5 V Schmitt Trigger,	 Current Strength: Default
-- ~ALTERA_TDI~	=>  Location: PIN_L4,	 I/O Standard: 2.5 V Schmitt Trigger,	 Current Strength: Default
-- ~ALTERA_TDO~	=>  Location: PIN_M5,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- ~ALTERA_CONFIG_SEL~	=>  Location: PIN_H10,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- ~ALTERA_nCONFIG~	=>  Location: PIN_H9,	 I/O Standard: 2.5 V Schmitt Trigger,	 Current Strength: Default
-- ~ALTERA_nSTATUS~	=>  Location: PIN_G9,	 I/O Standard: 2.5 V Schmitt Trigger,	 Current Strength: Default
-- ~ALTERA_CONF_DONE~	=>  Location: PIN_F8,	 I/O Standard: 2.5 V Schmitt Trigger,	 Current Strength: Default


ARCHITECTURE structure OF hard_block IS
SIGNAL gnd : std_logic := '0';
SIGNAL vcc : std_logic := '1';
SIGNAL unknown : std_logic := 'X';
SIGNAL ww_devoe : std_logic;
SIGNAL ww_devclrn : std_logic;
SIGNAL ww_devpor : std_logic;
SIGNAL \~ALTERA_TMS~~padout\ : std_logic;
SIGNAL \~ALTERA_TCK~~padout\ : std_logic;
SIGNAL \~ALTERA_TDI~~padout\ : std_logic;
SIGNAL \~ALTERA_CONFIG_SEL~~padout\ : std_logic;
SIGNAL \~ALTERA_nCONFIG~~padout\ : std_logic;
SIGNAL \~ALTERA_nSTATUS~~padout\ : std_logic;
SIGNAL \~ALTERA_CONF_DONE~~padout\ : std_logic;
SIGNAL \~ALTERA_TMS~~ibuf_o\ : std_logic;
SIGNAL \~ALTERA_TCK~~ibuf_o\ : std_logic;
SIGNAL \~ALTERA_TDI~~ibuf_o\ : std_logic;
SIGNAL \~ALTERA_CONFIG_SEL~~ibuf_o\ : std_logic;
SIGNAL \~ALTERA_nCONFIG~~ibuf_o\ : std_logic;
SIGNAL \~ALTERA_nSTATUS~~ibuf_o\ : std_logic;
SIGNAL \~ALTERA_CONF_DONE~~ibuf_o\ : std_logic;

BEGIN

ww_devoe <= devoe;
ww_devclrn <= devclrn;
ww_devpor <= devpor;
END structure;


LIBRARY FIFTYFIVENM;
LIBRARY IEEE;
USE FIFTYFIVENM.FIFTYFIVENM_COMPONENTS.ALL;
USE IEEE.STD_LOGIC_1164.ALL;

ENTITY 	HexMux IS
    PORT (
	sel : IN std_logic_vector(1 DOWNTO 0);
	bin : IN std_logic_vector(11 DOWNTO 0);
	tsseg : OUT std_logic_vector(20 DOWNTO 0)
	);
END HexMux;

-- Design Ports Information
-- tsseg[0]	=>  Location: PIN_Y8,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- tsseg[1]	=>  Location: PIN_V7,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- tsseg[2]	=>  Location: PIN_P9,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- tsseg[3]	=>  Location: PIN_R9,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- tsseg[4]	=>  Location: PIN_Y7,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- tsseg[5]	=>  Location: PIN_V8,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- tsseg[6]	=>  Location: PIN_Y4,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- tsseg[7]	=>  Location: PIN_B7,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- tsseg[8]	=>  Location: PIN_D7,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- tsseg[9]	=>  Location: PIN_A4,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- tsseg[10]	=>  Location: PIN_A6,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- tsseg[11]	=>  Location: PIN_B5,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- tsseg[12]	=>  Location: PIN_C6,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- tsseg[13]	=>  Location: PIN_B4,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- tsseg[14]	=>  Location: PIN_C7,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- tsseg[15]	=>  Location: PIN_C5,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- tsseg[16]	=>  Location: PIN_B2,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- tsseg[17]	=>  Location: PIN_B3,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- tsseg[18]	=>  Location: PIN_E11,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- tsseg[19]	=>  Location: PIN_E10,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- tsseg[20]	=>  Location: PIN_E9,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- sel[0]	=>  Location: PIN_C4,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- bin[0]	=>  Location: PIN_W9,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- bin[1]	=>  Location: PIN_Y3,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- bin[2]	=>  Location: PIN_AB2,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- bin[3]	=>  Location: PIN_W8,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- sel[1]	=>  Location: PIN_E8,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- bin[4]	=>  Location: PIN_D9,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- bin[5]	=>  Location: PIN_A5,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- bin[6]	=>  Location: PIN_J10,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- bin[7]	=>  Location: PIN_D8,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- bin[8]	=>  Location: PIN_A3,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- bin[9]	=>  Location: PIN_D10,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- bin[10]	=>  Location: PIN_H11,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- bin[11]	=>  Location: PIN_A2,	 I/O Standard: 2.5 V,	 Current Strength: Default


ARCHITECTURE structure OF HexMux IS
SIGNAL gnd : std_logic := '0';
SIGNAL vcc : std_logic := '1';
SIGNAL unknown : std_logic := 'X';
SIGNAL devoe : std_logic := '1';
SIGNAL devclrn : std_logic := '1';
SIGNAL devpor : std_logic := '1';
SIGNAL ww_devoe : std_logic;
SIGNAL ww_devclrn : std_logic;
SIGNAL ww_devpor : std_logic;
SIGNAL ww_sel : std_logic_vector(1 DOWNTO 0);
SIGNAL ww_bin : std_logic_vector(11 DOWNTO 0);
SIGNAL ww_tsseg : std_logic_vector(20 DOWNTO 0);
SIGNAL \~QUARTUS_CREATED_ADC1~_CHSEL_bus\ : std_logic_vector(4 DOWNTO 0);
SIGNAL \~QUARTUS_CREATED_ADC2~_CHSEL_bus\ : std_logic_vector(4 DOWNTO 0);
SIGNAL \~QUARTUS_CREATED_GND~I_combout\ : std_logic;
SIGNAL \~QUARTUS_CREATED_UNVM~~busy\ : std_logic;
SIGNAL \~QUARTUS_CREATED_ADC1~~eoc\ : std_logic;
SIGNAL \~QUARTUS_CREATED_ADC2~~eoc\ : std_logic;
SIGNAL \tsseg[0]~output_o\ : std_logic;
SIGNAL \tsseg[1]~output_o\ : std_logic;
SIGNAL \tsseg[2]~output_o\ : std_logic;
SIGNAL \tsseg[3]~output_o\ : std_logic;
SIGNAL \tsseg[4]~output_o\ : std_logic;
SIGNAL \tsseg[5]~output_o\ : std_logic;
SIGNAL \tsseg[6]~output_o\ : std_logic;
SIGNAL \tsseg[7]~output_o\ : std_logic;
SIGNAL \tsseg[8]~output_o\ : std_logic;
SIGNAL \tsseg[9]~output_o\ : std_logic;
SIGNAL \tsseg[10]~output_o\ : std_logic;
SIGNAL \tsseg[11]~output_o\ : std_logic;
SIGNAL \tsseg[12]~output_o\ : std_logic;
SIGNAL \tsseg[13]~output_o\ : std_logic;
SIGNAL \tsseg[14]~output_o\ : std_logic;
SIGNAL \tsseg[15]~output_o\ : std_logic;
SIGNAL \tsseg[16]~output_o\ : std_logic;
SIGNAL \tsseg[17]~output_o\ : std_logic;
SIGNAL \tsseg[18]~output_o\ : std_logic;
SIGNAL \tsseg[19]~output_o\ : std_logic;
SIGNAL \tsseg[20]~output_o\ : std_logic;
SIGNAL \bin[2]~input_o\ : std_logic;
SIGNAL \bin[0]~input_o\ : std_logic;
SIGNAL \bin[3]~input_o\ : std_logic;
SIGNAL \bin[1]~input_o\ : std_logic;
SIGNAL \bin2sevenseg|Mux6~0_combout\ : std_logic;
SIGNAL \sel[0]~input_o\ : std_logic;
SIGNAL \sel[1]~input_o\ : std_logic;
SIGNAL \Mux20~0_combout\ : std_logic;
SIGNAL \bin2sevenseg|Mux5~0_combout\ : std_logic;
SIGNAL \Mux19~0_combout\ : std_logic;
SIGNAL \bin2sevenseg|Mux4~0_combout\ : std_logic;
SIGNAL \Mux18~0_combout\ : std_logic;
SIGNAL \bin2sevenseg|Mux3~0_combout\ : std_logic;
SIGNAL \Mux17~0_combout\ : std_logic;
SIGNAL \bin2sevenseg|Mux2~0_combout\ : std_logic;
SIGNAL \Mux16~0_combout\ : std_logic;
SIGNAL \bin2sevenseg|Mux1~0_combout\ : std_logic;
SIGNAL \Mux15~0_combout\ : std_logic;
SIGNAL \bin2sevenseg|Mux0~0_combout\ : std_logic;
SIGNAL \Mux14~0_combout\ : std_logic;
SIGNAL \bin[4]~input_o\ : std_logic;
SIGNAL \bin[5]~input_o\ : std_logic;
SIGNAL \bin[7]~input_o\ : std_logic;
SIGNAL \bin[6]~input_o\ : std_logic;
SIGNAL \bin2sevenseg2|Mux6~0_combout\ : std_logic;
SIGNAL \Mux13~0_combout\ : std_logic;
SIGNAL \bin2sevenseg2|Mux5~0_combout\ : std_logic;
SIGNAL \Mux12~0_combout\ : std_logic;
SIGNAL \bin2sevenseg2|Mux4~0_combout\ : std_logic;
SIGNAL \Mux11~0_combout\ : std_logic;
SIGNAL \bin2sevenseg2|Mux3~0_combout\ : std_logic;
SIGNAL \Mux10~0_combout\ : std_logic;
SIGNAL \bin2sevenseg2|Mux2~0_combout\ : std_logic;
SIGNAL \Mux9~0_combout\ : std_logic;
SIGNAL \bin2sevenseg2|Mux1~0_combout\ : std_logic;
SIGNAL \Mux8~0_combout\ : std_logic;
SIGNAL \bin2sevenseg2|Mux0~0_combout\ : std_logic;
SIGNAL \Mux7~0_combout\ : std_logic;
SIGNAL \bin[8]~input_o\ : std_logic;
SIGNAL \bin[10]~input_o\ : std_logic;
SIGNAL \bin[11]~input_o\ : std_logic;
SIGNAL \bin[9]~input_o\ : std_logic;
SIGNAL \bin2sevenseg3|Mux6~0_combout\ : std_logic;
SIGNAL \Mux6~0_combout\ : std_logic;
SIGNAL \bin2sevenseg3|Mux5~0_combout\ : std_logic;
SIGNAL \Mux5~0_combout\ : std_logic;
SIGNAL \bin2sevenseg3|Mux4~0_combout\ : std_logic;
SIGNAL \Mux4~0_combout\ : std_logic;
SIGNAL \bin2sevenseg3|Mux3~0_combout\ : std_logic;
SIGNAL \Mux3~0_combout\ : std_logic;
SIGNAL \bin2sevenseg3|Mux2~0_combout\ : std_logic;
SIGNAL \Mux2~0_combout\ : std_logic;
SIGNAL \bin2sevenseg3|Mux1~0_combout\ : std_logic;
SIGNAL \Mux1~0_combout\ : std_logic;
SIGNAL \bin2sevenseg3|Mux0~0_combout\ : std_logic;
SIGNAL \Mux0~0_combout\ : std_logic;

COMPONENT hard_block
    PORT (
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic);
END COMPONENT;

BEGIN

ww_sel <= sel;
ww_bin <= bin;
tsseg <= ww_tsseg;
ww_devoe <= devoe;
ww_devclrn <= devclrn;
ww_devpor <= devpor;

\~QUARTUS_CREATED_ADC1~_CHSEL_bus\ <= (\~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\);

\~QUARTUS_CREATED_ADC2~_CHSEL_bus\ <= (\~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\);
auto_generated_inst : hard_block
PORT MAP (
	devoe => ww_devoe,
	devclrn => ww_devclrn,
	devpor => ww_devpor);

-- Location: LCCOMB_X44_Y49_N8
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

-- Location: IOOBUF_X20_Y0_N2
\tsseg[0]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \Mux20~0_combout\,
	devoe => ww_devoe,
	o => \tsseg[0]~output_o\);

-- Location: IOOBUF_X20_Y0_N23
\tsseg[1]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \Mux19~0_combout\,
	devoe => ww_devoe,
	o => \tsseg[1]~output_o\);

-- Location: IOOBUF_X22_Y0_N23
\tsseg[2]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \Mux18~0_combout\,
	devoe => ww_devoe,
	o => \tsseg[2]~output_o\);

-- Location: IOOBUF_X22_Y0_N30
\tsseg[3]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \Mux17~0_combout\,
	devoe => ww_devoe,
	o => \tsseg[3]~output_o\);

-- Location: IOOBUF_X20_Y0_N9
\tsseg[4]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \Mux16~0_combout\,
	devoe => ww_devoe,
	o => \tsseg[4]~output_o\);

-- Location: IOOBUF_X20_Y0_N16
\tsseg[5]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \Mux15~0_combout\,
	devoe => ww_devoe,
	o => \tsseg[5]~output_o\);

-- Location: IOOBUF_X24_Y0_N16
\tsseg[6]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \Mux14~0_combout\,
	devoe => ww_devoe,
	o => \tsseg[6]~output_o\);

-- Location: IOOBUF_X34_Y39_N23
\tsseg[7]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \Mux13~0_combout\,
	devoe => ww_devoe,
	o => \tsseg[7]~output_o\);

-- Location: IOOBUF_X29_Y39_N16
\tsseg[8]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \Mux12~0_combout\,
	devoe => ww_devoe,
	o => \tsseg[8]~output_o\);

-- Location: IOOBUF_X31_Y39_N23
\tsseg[9]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \Mux11~0_combout\,
	devoe => ww_devoe,
	o => \tsseg[9]~output_o\);

-- Location: IOOBUF_X34_Y39_N30
\tsseg[10]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \Mux10~0_combout\,
	devoe => ww_devoe,
	o => \tsseg[10]~output_o\);

-- Location: IOOBUF_X26_Y39_N30
\tsseg[11]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \Mux9~0_combout\,
	devoe => ww_devoe,
	o => \tsseg[11]~output_o\);

-- Location: IOOBUF_X29_Y39_N9
\tsseg[12]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \Mux8~0_combout\,
	devoe => ww_devoe,
	o => \tsseg[12]~output_o\);

-- Location: IOOBUF_X26_Y39_N23
\tsseg[13]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \Mux7~0_combout\,
	devoe => ww_devoe,
	o => \tsseg[13]~output_o\);

-- Location: IOOBUF_X34_Y39_N2
\tsseg[14]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \Mux6~0_combout\,
	devoe => ww_devoe,
	o => \tsseg[14]~output_o\);

-- Location: IOOBUF_X24_Y39_N23
\tsseg[15]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \Mux5~0_combout\,
	devoe => ww_devoe,
	o => \tsseg[15]~output_o\);

-- Location: IOOBUF_X22_Y39_N16
\tsseg[16]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \Mux4~0_combout\,
	devoe => ww_devoe,
	o => \tsseg[16]~output_o\);

-- Location: IOOBUF_X26_Y39_N16
\tsseg[17]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \Mux3~0_combout\,
	devoe => ww_devoe,
	o => \tsseg[17]~output_o\);

-- Location: IOOBUF_X36_Y39_N16
\tsseg[18]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \Mux2~0_combout\,
	devoe => ww_devoe,
	o => \tsseg[18]~output_o\);

-- Location: IOOBUF_X36_Y39_N23
\tsseg[19]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \Mux1~0_combout\,
	devoe => ww_devoe,
	o => \tsseg[19]~output_o\);

-- Location: IOOBUF_X29_Y39_N2
\tsseg[20]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \Mux0~0_combout\,
	devoe => ww_devoe,
	o => \tsseg[20]~output_o\);

-- Location: IOIBUF_X22_Y0_N15
\bin[2]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_bin(2),
	o => \bin[2]~input_o\);

-- Location: IOIBUF_X22_Y0_N1
\bin[0]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_bin(0),
	o => \bin[0]~input_o\);

-- Location: IOIBUF_X24_Y0_N1
\bin[3]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_bin(3),
	o => \bin[3]~input_o\);

-- Location: IOIBUF_X24_Y0_N22
\bin[1]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_bin(1),
	o => \bin[1]~input_o\);

-- Location: LCCOMB_X22_Y4_N24
\bin2sevenseg|Mux6~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \bin2sevenseg|Mux6~0_combout\ = (\bin[2]~input_o\ & (!\bin[1]~input_o\ & (\bin[0]~input_o\ $ (!\bin[3]~input_o\)))) # (!\bin[2]~input_o\ & (\bin[0]~input_o\ & (\bin[3]~input_o\ $ (!\bin[1]~input_o\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0100000010000110",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \bin[2]~input_o\,
	datab => \bin[0]~input_o\,
	datac => \bin[3]~input_o\,
	datad => \bin[1]~input_o\,
	combout => \bin2sevenseg|Mux6~0_combout\);

-- Location: IOIBUF_X24_Y39_N1
\sel[0]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_sel(0),
	o => \sel[0]~input_o\);

-- Location: IOIBUF_X24_Y39_N8
\sel[1]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_sel(1),
	o => \sel[1]~input_o\);

-- Location: LCCOMB_X22_Y4_N10
\Mux20~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux20~0_combout\ = (\bin2sevenseg|Mux6~0_combout\) # ((\sel[0]~input_o\) # (!\sel[1]~input_o\))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111110011111111",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datab => \bin2sevenseg|Mux6~0_combout\,
	datac => \sel[0]~input_o\,
	datad => \sel[1]~input_o\,
	combout => \Mux20~0_combout\);

-- Location: LCCOMB_X22_Y4_N12
\bin2sevenseg|Mux5~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \bin2sevenseg|Mux5~0_combout\ = (\bin[3]~input_o\ & ((\bin[0]~input_o\ & ((\bin[1]~input_o\))) # (!\bin[0]~input_o\ & (\bin[2]~input_o\)))) # (!\bin[3]~input_o\ & (\bin[2]~input_o\ & (\bin[0]~input_o\ $ (\bin[1]~input_o\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1110001000101000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \bin[2]~input_o\,
	datab => \bin[0]~input_o\,
	datac => \bin[3]~input_o\,
	datad => \bin[1]~input_o\,
	combout => \bin2sevenseg|Mux5~0_combout\);

-- Location: LCCOMB_X22_Y4_N30
\Mux19~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux19~0_combout\ = (\bin2sevenseg|Mux5~0_combout\) # ((\sel[0]~input_o\) # (!\sel[1]~input_o\))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111101011111111",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \bin2sevenseg|Mux5~0_combout\,
	datac => \sel[0]~input_o\,
	datad => \sel[1]~input_o\,
	combout => \Mux19~0_combout\);

-- Location: LCCOMB_X22_Y4_N0
\bin2sevenseg|Mux4~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \bin2sevenseg|Mux4~0_combout\ = (\bin[2]~input_o\ & (\bin[3]~input_o\ & ((\bin[1]~input_o\) # (!\bin[0]~input_o\)))) # (!\bin[2]~input_o\ & (!\bin[0]~input_o\ & (!\bin[3]~input_o\ & \bin[1]~input_o\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1010000100100000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \bin[2]~input_o\,
	datab => \bin[0]~input_o\,
	datac => \bin[3]~input_o\,
	datad => \bin[1]~input_o\,
	combout => \bin2sevenseg|Mux4~0_combout\);

-- Location: LCCOMB_X22_Y4_N18
\Mux18~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux18~0_combout\ = ((\bin2sevenseg|Mux4~0_combout\ & !\sel[0]~input_o\)) # (!\sel[1]~input_o\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0000110011111111",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datab => \bin2sevenseg|Mux4~0_combout\,
	datac => \sel[0]~input_o\,
	datad => \sel[1]~input_o\,
	combout => \Mux18~0_combout\);

-- Location: LCCOMB_X22_Y4_N20
\bin2sevenseg|Mux3~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \bin2sevenseg|Mux3~0_combout\ = (\bin[1]~input_o\ & ((\bin[2]~input_o\ & (\bin[0]~input_o\)) # (!\bin[2]~input_o\ & (!\bin[0]~input_o\ & \bin[3]~input_o\)))) # (!\bin[1]~input_o\ & (!\bin[3]~input_o\ & (\bin[2]~input_o\ $ (\bin[0]~input_o\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1001100000000110",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \bin[2]~input_o\,
	datab => \bin[0]~input_o\,
	datac => \bin[3]~input_o\,
	datad => \bin[1]~input_o\,
	combout => \bin2sevenseg|Mux3~0_combout\);

-- Location: LCCOMB_X22_Y4_N6
\Mux17~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux17~0_combout\ = (\bin2sevenseg|Mux3~0_combout\) # ((\sel[0]~input_o\) # (!\sel[1]~input_o\))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111110011111111",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datab => \bin2sevenseg|Mux3~0_combout\,
	datac => \sel[0]~input_o\,
	datad => \sel[1]~input_o\,
	combout => \Mux17~0_combout\);

-- Location: LCCOMB_X22_Y4_N8
\bin2sevenseg|Mux2~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \bin2sevenseg|Mux2~0_combout\ = (\bin[1]~input_o\ & (((\bin[0]~input_o\ & !\bin[3]~input_o\)))) # (!\bin[1]~input_o\ & ((\bin[2]~input_o\ & ((!\bin[3]~input_o\))) # (!\bin[2]~input_o\ & (\bin[0]~input_o\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0000110001001110",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \bin[2]~input_o\,
	datab => \bin[0]~input_o\,
	datac => \bin[3]~input_o\,
	datad => \bin[1]~input_o\,
	combout => \bin2sevenseg|Mux2~0_combout\);

-- Location: LCCOMB_X22_Y4_N26
\Mux16~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux16~0_combout\ = (!\sel[0]~input_o\ & ((\bin2sevenseg|Mux2~0_combout\) # (!\sel[1]~input_o\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0011000000110011",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datab => \sel[0]~input_o\,
	datac => \bin2sevenseg|Mux2~0_combout\,
	datad => \sel[1]~input_o\,
	combout => \Mux16~0_combout\);

-- Location: LCCOMB_X22_Y4_N28
\bin2sevenseg|Mux1~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \bin2sevenseg|Mux1~0_combout\ = (\bin[2]~input_o\ & (\bin[0]~input_o\ & (\bin[3]~input_o\ $ (\bin[1]~input_o\)))) # (!\bin[2]~input_o\ & (!\bin[3]~input_o\ & ((\bin[0]~input_o\) # (\bin[1]~input_o\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0000110110000100",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \bin[2]~input_o\,
	datab => \bin[0]~input_o\,
	datac => \bin[3]~input_o\,
	datad => \bin[1]~input_o\,
	combout => \bin2sevenseg|Mux1~0_combout\);

-- Location: LCCOMB_X22_Y4_N22
\Mux15~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux15~0_combout\ = (\bin2sevenseg|Mux1~0_combout\) # ((\sel[0]~input_o\) # (!\sel[1]~input_o\))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111110011111111",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datab => \bin2sevenseg|Mux1~0_combout\,
	datac => \sel[0]~input_o\,
	datad => \sel[1]~input_o\,
	combout => \Mux15~0_combout\);

-- Location: LCCOMB_X22_Y4_N16
\bin2sevenseg|Mux0~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \bin2sevenseg|Mux0~0_combout\ = (\bin[0]~input_o\ & ((\bin[3]~input_o\) # (\bin[2]~input_o\ $ (\bin[1]~input_o\)))) # (!\bin[0]~input_o\ & ((\bin[1]~input_o\) # (\bin[2]~input_o\ $ (\bin[3]~input_o\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111011111011010",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \bin[2]~input_o\,
	datab => \bin[0]~input_o\,
	datac => \bin[3]~input_o\,
	datad => \bin[1]~input_o\,
	combout => \bin2sevenseg|Mux0~0_combout\);

-- Location: LCCOMB_X22_Y4_N2
\Mux14~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux14~0_combout\ = (!\sel[0]~input_o\ & ((!\sel[1]~input_o\) # (!\bin2sevenseg|Mux0~0_combout\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0000001100001111",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datab => \bin2sevenseg|Mux0~0_combout\,
	datac => \sel[0]~input_o\,
	datad => \sel[1]~input_o\,
	combout => \Mux14~0_combout\);

-- Location: IOIBUF_X31_Y39_N8
\bin[4]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_bin(4),
	o => \bin[4]~input_o\);

-- Location: IOIBUF_X31_Y39_N15
\bin[5]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_bin(5),
	o => \bin[5]~input_o\);

-- Location: IOIBUF_X31_Y39_N1
\bin[7]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_bin(7),
	o => \bin[7]~input_o\);

-- Location: IOIBUF_X34_Y39_N8
\bin[6]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_bin(6),
	o => \bin[6]~input_o\);

-- Location: LCCOMB_X30_Y35_N24
\bin2sevenseg2|Mux6~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \bin2sevenseg2|Mux6~0_combout\ = (\bin[7]~input_o\ & (\bin[4]~input_o\ & (\bin[5]~input_o\ $ (\bin[6]~input_o\)))) # (!\bin[7]~input_o\ & (!\bin[5]~input_o\ & (\bin[4]~input_o\ $ (\bin[6]~input_o\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0010000110000010",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \bin[4]~input_o\,
	datab => \bin[5]~input_o\,
	datac => \bin[7]~input_o\,
	datad => \bin[6]~input_o\,
	combout => \bin2sevenseg2|Mux6~0_combout\);

-- Location: LCCOMB_X30_Y35_N10
\Mux13~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux13~0_combout\ = ((!\sel[0]~input_o\ & \bin2sevenseg2|Mux6~0_combout\)) # (!\sel[1]~input_o\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0101111101010101",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \sel[1]~input_o\,
	datac => \sel[0]~input_o\,
	datad => \bin2sevenseg2|Mux6~0_combout\,
	combout => \Mux13~0_combout\);

-- Location: LCCOMB_X30_Y35_N28
\bin2sevenseg2|Mux5~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \bin2sevenseg2|Mux5~0_combout\ = (\bin[5]~input_o\ & ((\bin[4]~input_o\ & (\bin[7]~input_o\)) # (!\bin[4]~input_o\ & ((\bin[6]~input_o\))))) # (!\bin[5]~input_o\ & (\bin[6]~input_o\ & (\bin[4]~input_o\ $ (\bin[7]~input_o\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1101011010000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \bin[4]~input_o\,
	datab => \bin[5]~input_o\,
	datac => \bin[7]~input_o\,
	datad => \bin[6]~input_o\,
	combout => \bin2sevenseg2|Mux5~0_combout\);

-- Location: LCCOMB_X30_Y35_N22
\Mux12~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux12~0_combout\ = ((!\sel[0]~input_o\ & \bin2sevenseg2|Mux5~0_combout\)) # (!\sel[1]~input_o\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0101111101010101",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \sel[1]~input_o\,
	datac => \sel[0]~input_o\,
	datad => \bin2sevenseg2|Mux5~0_combout\,
	combout => \Mux12~0_combout\);

-- Location: LCCOMB_X30_Y35_N8
\bin2sevenseg2|Mux4~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \bin2sevenseg2|Mux4~0_combout\ = (\bin[7]~input_o\ & (\bin[6]~input_o\ & ((\bin[5]~input_o\) # (!\bin[4]~input_o\)))) # (!\bin[7]~input_o\ & (!\bin[4]~input_o\ & (\bin[5]~input_o\ & !\bin[6]~input_o\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1101000000000100",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \bin[4]~input_o\,
	datab => \bin[5]~input_o\,
	datac => \bin[7]~input_o\,
	datad => \bin[6]~input_o\,
	combout => \bin2sevenseg2|Mux4~0_combout\);

-- Location: LCCOMB_X30_Y35_N2
\Mux11~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux11~0_combout\ = ((\bin2sevenseg2|Mux4~0_combout\ & !\sel[0]~input_o\)) # (!\sel[1]~input_o\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0101110101011101",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \sel[1]~input_o\,
	datab => \bin2sevenseg2|Mux4~0_combout\,
	datac => \sel[0]~input_o\,
	combout => \Mux11~0_combout\);

-- Location: LCCOMB_X30_Y35_N20
\bin2sevenseg2|Mux3~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \bin2sevenseg2|Mux3~0_combout\ = (\bin[5]~input_o\ & ((\bin[4]~input_o\ & ((\bin[6]~input_o\))) # (!\bin[4]~input_o\ & (\bin[7]~input_o\ & !\bin[6]~input_o\)))) # (!\bin[5]~input_o\ & (!\bin[7]~input_o\ & (\bin[4]~input_o\ $ (\bin[6]~input_o\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1000100101000010",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \bin[4]~input_o\,
	datab => \bin[5]~input_o\,
	datac => \bin[7]~input_o\,
	datad => \bin[6]~input_o\,
	combout => \bin2sevenseg2|Mux3~0_combout\);

-- Location: LCCOMB_X30_Y35_N30
\Mux10~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux10~0_combout\ = ((!\sel[0]~input_o\ & \bin2sevenseg2|Mux3~0_combout\)) # (!\sel[1]~input_o\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0101111101010101",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \sel[1]~input_o\,
	datac => \sel[0]~input_o\,
	datad => \bin2sevenseg2|Mux3~0_combout\,
	combout => \Mux10~0_combout\);

-- Location: LCCOMB_X30_Y35_N0
\bin2sevenseg2|Mux2~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \bin2sevenseg2|Mux2~0_combout\ = (\bin[5]~input_o\ & (\bin[4]~input_o\ & (!\bin[7]~input_o\))) # (!\bin[5]~input_o\ & ((\bin[6]~input_o\ & ((!\bin[7]~input_o\))) # (!\bin[6]~input_o\ & (\bin[4]~input_o\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0000101100101010",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \bin[4]~input_o\,
	datab => \bin[5]~input_o\,
	datac => \bin[7]~input_o\,
	datad => \bin[6]~input_o\,
	combout => \bin2sevenseg2|Mux2~0_combout\);

-- Location: LCCOMB_X30_Y36_N0
\Mux9~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux9~0_combout\ = (!\sel[0]~input_o\ & ((\bin2sevenseg2|Mux2~0_combout\) # (!\sel[1]~input_o\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0000111100000101",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \sel[1]~input_o\,
	datac => \sel[0]~input_o\,
	datad => \bin2sevenseg2|Mux2~0_combout\,
	combout => \Mux9~0_combout\);

-- Location: LCCOMB_X30_Y35_N18
\bin2sevenseg2|Mux1~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \bin2sevenseg2|Mux1~0_combout\ = (\bin[4]~input_o\ & (\bin[7]~input_o\ $ (((\bin[5]~input_o\) # (!\bin[6]~input_o\))))) # (!\bin[4]~input_o\ & (\bin[5]~input_o\ & (!\bin[7]~input_o\ & !\bin[6]~input_o\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0010100000001110",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \bin[4]~input_o\,
	datab => \bin[5]~input_o\,
	datac => \bin[7]~input_o\,
	datad => \bin[6]~input_o\,
	combout => \bin2sevenseg2|Mux1~0_combout\);

-- Location: LCCOMB_X30_Y35_N12
\Mux8~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux8~0_combout\ = ((!\sel[0]~input_o\ & \bin2sevenseg2|Mux1~0_combout\)) # (!\sel[1]~input_o\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0101111101010101",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \sel[1]~input_o\,
	datac => \sel[0]~input_o\,
	datad => \bin2sevenseg2|Mux1~0_combout\,
	combout => \Mux8~0_combout\);

-- Location: LCCOMB_X30_Y35_N14
\bin2sevenseg2|Mux0~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \bin2sevenseg2|Mux0~0_combout\ = (\bin[4]~input_o\ & ((\bin[7]~input_o\) # (\bin[5]~input_o\ $ (\bin[6]~input_o\)))) # (!\bin[4]~input_o\ & ((\bin[5]~input_o\) # (\bin[7]~input_o\ $ (\bin[6]~input_o\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1110011111111100",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \bin[4]~input_o\,
	datab => \bin[5]~input_o\,
	datac => \bin[7]~input_o\,
	datad => \bin[6]~input_o\,
	combout => \bin2sevenseg2|Mux0~0_combout\);

-- Location: LCCOMB_X30_Y36_N26
\Mux7~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux7~0_combout\ = (\sel[1]~input_o\ & ((\sel[0]~input_o\) # (!\bin2sevenseg2|Mux0~0_combout\))) # (!\sel[1]~input_o\ & ((!\sel[0]~input_o\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1010011110100111",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \sel[1]~input_o\,
	datab => \bin2sevenseg2|Mux0~0_combout\,
	datac => \sel[0]~input_o\,
	combout => \Mux7~0_combout\);

-- Location: IOIBUF_X26_Y39_N8
\bin[8]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_bin(8),
	o => \bin[8]~input_o\);

-- Location: IOIBUF_X34_Y39_N15
\bin[10]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_bin(10),
	o => \bin[10]~input_o\);

-- Location: IOIBUF_X26_Y39_N1
\bin[11]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_bin(11),
	o => \bin[11]~input_o\);

-- Location: IOIBUF_X31_Y39_N29
\bin[9]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_bin(9),
	o => \bin[9]~input_o\);

-- Location: LCCOMB_X30_Y36_N4
\bin2sevenseg3|Mux6~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \bin2sevenseg3|Mux6~0_combout\ = (\bin[10]~input_o\ & (!\bin[9]~input_o\ & (\bin[8]~input_o\ $ (!\bin[11]~input_o\)))) # (!\bin[10]~input_o\ & (\bin[8]~input_o\ & (\bin[11]~input_o\ $ (!\bin[9]~input_o\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0010000010000110",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \bin[8]~input_o\,
	datab => \bin[10]~input_o\,
	datac => \bin[11]~input_o\,
	datad => \bin[9]~input_o\,
	combout => \bin2sevenseg3|Mux6~0_combout\);

-- Location: LCCOMB_X30_Y36_N30
\Mux6~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux6~0_combout\ = (\sel[1]~input_o\ & ((\bin2sevenseg3|Mux6~0_combout\) # (\sel[0]~input_o\))) # (!\sel[1]~input_o\ & ((!\sel[0]~input_o\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1010110110101101",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \sel[1]~input_o\,
	datab => \bin2sevenseg3|Mux6~0_combout\,
	datac => \sel[0]~input_o\,
	combout => \Mux6~0_combout\);

-- Location: LCCOMB_X30_Y36_N24
\bin2sevenseg3|Mux5~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \bin2sevenseg3|Mux5~0_combout\ = (\bin[11]~input_o\ & ((\bin[8]~input_o\ & ((\bin[9]~input_o\))) # (!\bin[8]~input_o\ & (\bin[10]~input_o\)))) # (!\bin[11]~input_o\ & (\bin[10]~input_o\ & (\bin[8]~input_o\ $ (\bin[9]~input_o\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1110010001001000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \bin[8]~input_o\,
	datab => \bin[10]~input_o\,
	datac => \bin[11]~input_o\,
	datad => \bin[9]~input_o\,
	combout => \bin2sevenseg3|Mux5~0_combout\);

-- Location: LCCOMB_X30_Y36_N2
\Mux5~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux5~0_combout\ = ((\sel[0]~input_o\) # (\bin2sevenseg3|Mux5~0_combout\)) # (!\sel[1]~input_o\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111111111110101",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \sel[1]~input_o\,
	datac => \sel[0]~input_o\,
	datad => \bin2sevenseg3|Mux5~0_combout\,
	combout => \Mux5~0_combout\);

-- Location: LCCOMB_X30_Y36_N12
\bin2sevenseg3|Mux4~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \bin2sevenseg3|Mux4~0_combout\ = (\bin[10]~input_o\ & (\bin[11]~input_o\ & ((\bin[9]~input_o\) # (!\bin[8]~input_o\)))) # (!\bin[10]~input_o\ & (!\bin[8]~input_o\ & (!\bin[11]~input_o\ & \bin[9]~input_o\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1100000101000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \bin[8]~input_o\,
	datab => \bin[10]~input_o\,
	datac => \bin[11]~input_o\,
	datad => \bin[9]~input_o\,
	combout => \bin2sevenseg3|Mux4~0_combout\);

-- Location: LCCOMB_X30_Y36_N22
\Mux4~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux4~0_combout\ = ((\sel[0]~input_o\) # (\bin2sevenseg3|Mux4~0_combout\)) # (!\sel[1]~input_o\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111111111110101",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \sel[1]~input_o\,
	datac => \sel[0]~input_o\,
	datad => \bin2sevenseg3|Mux4~0_combout\,
	combout => \Mux4~0_combout\);

-- Location: LCCOMB_X30_Y36_N8
\bin2sevenseg3|Mux3~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \bin2sevenseg3|Mux3~0_combout\ = (\bin[9]~input_o\ & ((\bin[8]~input_o\ & (\bin[10]~input_o\)) # (!\bin[8]~input_o\ & (!\bin[10]~input_o\ & \bin[11]~input_o\)))) # (!\bin[9]~input_o\ & (!\bin[11]~input_o\ & (\bin[8]~input_o\ $ (\bin[10]~input_o\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1001100000000110",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \bin[8]~input_o\,
	datab => \bin[10]~input_o\,
	datac => \bin[11]~input_o\,
	datad => \bin[9]~input_o\,
	combout => \bin2sevenseg3|Mux3~0_combout\);

-- Location: LCCOMB_X30_Y36_N18
\Mux3~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux3~0_combout\ = (\sel[1]~input_o\ & ((\bin2sevenseg3|Mux3~0_combout\) # (\sel[0]~input_o\))) # (!\sel[1]~input_o\ & ((!\sel[0]~input_o\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1010110110101101",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \sel[1]~input_o\,
	datab => \bin2sevenseg3|Mux3~0_combout\,
	datac => \sel[0]~input_o\,
	combout => \Mux3~0_combout\);

-- Location: LCCOMB_X30_Y36_N20
\bin2sevenseg3|Mux2~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \bin2sevenseg3|Mux2~0_combout\ = (\bin[9]~input_o\ & (\bin[8]~input_o\ & ((!\bin[11]~input_o\)))) # (!\bin[9]~input_o\ & ((\bin[10]~input_o\ & ((!\bin[11]~input_o\))) # (!\bin[10]~input_o\ & (\bin[8]~input_o\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0000101000101110",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \bin[8]~input_o\,
	datab => \bin[10]~input_o\,
	datac => \bin[11]~input_o\,
	datad => \bin[9]~input_o\,
	combout => \bin2sevenseg3|Mux2~0_combout\);

-- Location: LCCOMB_X30_Y36_N6
\Mux2~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux2~0_combout\ = (\sel[1]~input_o\ & ((\sel[0]~input_o\) # (\bin2sevenseg3|Mux2~0_combout\))) # (!\sel[1]~input_o\ & (!\sel[0]~input_o\))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1010111110100101",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \sel[1]~input_o\,
	datac => \sel[0]~input_o\,
	datad => \bin2sevenseg3|Mux2~0_combout\,
	combout => \Mux2~0_combout\);

-- Location: LCCOMB_X30_Y36_N16
\bin2sevenseg3|Mux1~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \bin2sevenseg3|Mux1~0_combout\ = (\bin[8]~input_o\ & (\bin[11]~input_o\ $ (((\bin[9]~input_o\) # (!\bin[10]~input_o\))))) # (!\bin[8]~input_o\ & (!\bin[10]~input_o\ & (!\bin[11]~input_o\ & \bin[9]~input_o\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0000101110000010",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \bin[8]~input_o\,
	datab => \bin[10]~input_o\,
	datac => \bin[11]~input_o\,
	datad => \bin[9]~input_o\,
	combout => \bin2sevenseg3|Mux1~0_combout\);

-- Location: LCCOMB_X30_Y36_N10
\Mux1~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux1~0_combout\ = (\sel[1]~input_o\ & ((\sel[0]~input_o\) # (\bin2sevenseg3|Mux1~0_combout\))) # (!\sel[1]~input_o\ & (!\sel[0]~input_o\))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1010111110100101",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \sel[1]~input_o\,
	datac => \sel[0]~input_o\,
	datad => \bin2sevenseg3|Mux1~0_combout\,
	combout => \Mux1~0_combout\);

-- Location: LCCOMB_X30_Y36_N28
\bin2sevenseg3|Mux0~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \bin2sevenseg3|Mux0~0_combout\ = (\bin[8]~input_o\ & ((\bin[11]~input_o\) # (\bin[10]~input_o\ $ (\bin[9]~input_o\)))) # (!\bin[8]~input_o\ & ((\bin[9]~input_o\) # (\bin[10]~input_o\ $ (\bin[11]~input_o\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111011110111100",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \bin[8]~input_o\,
	datab => \bin[10]~input_o\,
	datac => \bin[11]~input_o\,
	datad => \bin[9]~input_o\,
	combout => \bin2sevenseg3|Mux0~0_combout\);

-- Location: LCCOMB_X30_Y36_N14
\Mux0~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux0~0_combout\ = (\sel[1]~input_o\ & ((\sel[0]~input_o\) # (!\bin2sevenseg3|Mux0~0_combout\))) # (!\sel[1]~input_o\ & (!\sel[0]~input_o\))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1010010110101111",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \sel[1]~input_o\,
	datac => \sel[0]~input_o\,
	datad => \bin2sevenseg3|Mux0~0_combout\,
	combout => \Mux0~0_combout\);

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

ww_tsseg(0) <= \tsseg[0]~output_o\;

ww_tsseg(1) <= \tsseg[1]~output_o\;

ww_tsseg(2) <= \tsseg[2]~output_o\;

ww_tsseg(3) <= \tsseg[3]~output_o\;

ww_tsseg(4) <= \tsseg[4]~output_o\;

ww_tsseg(5) <= \tsseg[5]~output_o\;

ww_tsseg(6) <= \tsseg[6]~output_o\;

ww_tsseg(7) <= \tsseg[7]~output_o\;

ww_tsseg(8) <= \tsseg[8]~output_o\;

ww_tsseg(9) <= \tsseg[9]~output_o\;

ww_tsseg(10) <= \tsseg[10]~output_o\;

ww_tsseg(11) <= \tsseg[11]~output_o\;

ww_tsseg(12) <= \tsseg[12]~output_o\;

ww_tsseg(13) <= \tsseg[13]~output_o\;

ww_tsseg(14) <= \tsseg[14]~output_o\;

ww_tsseg(15) <= \tsseg[15]~output_o\;

ww_tsseg(16) <= \tsseg[16]~output_o\;

ww_tsseg(17) <= \tsseg[17]~output_o\;

ww_tsseg(18) <= \tsseg[18]~output_o\;

ww_tsseg(19) <= \tsseg[19]~output_o\;

ww_tsseg(20) <= \tsseg[20]~output_o\;
END structure;


