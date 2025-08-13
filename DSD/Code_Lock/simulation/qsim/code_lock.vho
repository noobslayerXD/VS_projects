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

-- DATE "11/30/2023 19:09:45"

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


LIBRARY ALTERA;
LIBRARY FIFTYFIVENM;
LIBRARY IEEE;
USE ALTERA.ALTERA_PRIMITIVES_COMPONENTS.ALL;
USE FIFTYFIVENM.FIFTYFIVENM_COMPONENTS.ALL;
USE IEEE.STD_LOGIC_1164.ALL;

ENTITY 	code_lock_simple IS
    PORT (
	clk : IN std_logic;
	reset : IN std_logic;
	code : IN std_logic_vector(3 DOWNTO 0);
	enter : IN std_logic;
	err_count : OUT std_logic_vector(1 DOWNTO 0);
	lock : OUT std_logic;
	lock0 : OUT std_logic
	);
END code_lock_simple;

-- Design Ports Information
-- err_count[0]	=>  Location: PIN_P3,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- err_count[1]	=>  Location: PIN_M1,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- lock	=>  Location: PIN_N2,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- lock0	=>  Location: PIN_M9,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- reset	=>  Location: PIN_R3,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- clk	=>  Location: PIN_M8,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- code[1]	=>  Location: PIN_P1,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- code[2]	=>  Location: PIN_N9,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- code[3]	=>  Location: PIN_N1,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- code[0]	=>  Location: PIN_N8,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- enter	=>  Location: PIN_N3,	 I/O Standard: 2.5 V,	 Current Strength: Default


ARCHITECTURE structure OF code_lock_simple IS
SIGNAL gnd : std_logic := '0';
SIGNAL vcc : std_logic := '1';
SIGNAL unknown : std_logic := 'X';
SIGNAL devoe : std_logic := '1';
SIGNAL devclrn : std_logic := '1';
SIGNAL devpor : std_logic := '1';
SIGNAL ww_devoe : std_logic;
SIGNAL ww_devclrn : std_logic;
SIGNAL ww_devpor : std_logic;
SIGNAL ww_clk : std_logic;
SIGNAL ww_reset : std_logic;
SIGNAL ww_code : std_logic_vector(3 DOWNTO 0);
SIGNAL ww_enter : std_logic;
SIGNAL ww_err_count : std_logic_vector(1 DOWNTO 0);
SIGNAL ww_lock : std_logic;
SIGNAL ww_lock0 : std_logic;
SIGNAL \~QUARTUS_CREATED_ADC1~_CHSEL_bus\ : std_logic_vector(4 DOWNTO 0);
SIGNAL \~QUARTUS_CREATED_ADC2~_CHSEL_bus\ : std_logic_vector(4 DOWNTO 0);
SIGNAL \clk~inputclkctrl_INCLK_bus\ : std_logic_vector(3 DOWNTO 0);
SIGNAL \~QUARTUS_CREATED_GND~I_combout\ : std_logic;
SIGNAL \~QUARTUS_CREATED_UNVM~~busy\ : std_logic;
SIGNAL \~QUARTUS_CREATED_ADC1~~eoc\ : std_logic;
SIGNAL \~QUARTUS_CREATED_ADC2~~eoc\ : std_logic;
SIGNAL \err_count[0]~output_o\ : std_logic;
SIGNAL \err_count[1]~output_o\ : std_logic;
SIGNAL \lock~output_o\ : std_logic;
SIGNAL \lock0~output_o\ : std_logic;
SIGNAL \clk~input_o\ : std_logic;
SIGNAL \clk~inputclkctrl_outclk\ : std_logic;
SIGNAL \code[3]~input_o\ : std_logic;
SIGNAL \code[0]~input_o\ : std_logic;
SIGNAL \code[1]~input_o\ : std_logic;
SIGNAL \code[2]~input_o\ : std_logic;
SIGNAL \fsm|Equal3~0_combout\ : std_logic;
SIGNAL \reset~input_o\ : std_logic;
SIGNAL \enter~input_o\ : std_logic;
SIGNAL \synchronizer|sync1:resync[1]~0_combout\ : std_logic;
SIGNAL \synchronizer|sync1:resync[1]~q\ : std_logic;
SIGNAL \synchronizer|sync1:resync[2]~feeder_combout\ : std_logic;
SIGNAL \synchronizer|sync1:resync[2]~q\ : std_logic;
SIGNAL \synchronizer|sync1:resync[3]~feeder_combout\ : std_logic;
SIGNAL \synchronizer|sync1:resync[3]~q\ : std_logic;
SIGNAL \synchronizer|fall~0_combout\ : std_logic;
SIGNAL \synchronizer|fall~q\ : std_logic;
SIGNAL \fsm|present_state~14_combout\ : std_logic;
SIGNAL \fsm|Equal1~0_combout\ : std_logic;
SIGNAL \fsm|present_state~20_combout\ : std_logic;
SIGNAL \fsm|present_state~21_combout\ : std_logic;
SIGNAL \fsm|present_state.wrong_code~q\ : std_logic;
SIGNAL \fsm|present_state~16_combout\ : std_logic;
SIGNAL \fsm|present_state~17_combout\ : std_logic;
SIGNAL \fsm|present_state.idle~q\ : std_logic;
SIGNAL \fsm|present_state~15_combout\ : std_logic;
SIGNAL \fsm|present_state.Ev_code1~q\ : std_logic;
SIGNAL \fsm|present_state~19_combout\ : std_logic;
SIGNAL \fsm|present_state.get_code2~q\ : std_logic;
SIGNAL \fsm|present_state~13_combout\ : std_logic;
SIGNAL \fsm|present_state.Ev_code2~q\ : std_logic;
SIGNAL \fsm|lock~0_combout\ : std_logic;
SIGNAL \fsm|present_state~18_combout\ : std_logic;
SIGNAL \fsm|present_state.Unlocked~q\ : std_logic;
SIGNAL \fsm|Selector0~0_combout\ : std_logic;
SIGNAL \fsm|err_event~combout\ : std_logic;
SIGNAL \Wrong|present_state~7_combout\ : std_logic;
SIGNAL \Wrong|present_state.idle~q\ : std_logic;
SIGNAL \Wrong|present_state~6_combout\ : std_logic;
SIGNAL \Wrong|present_state.err_state0~q\ : std_logic;
SIGNAL \Wrong|present_state~9_combout\ : std_logic;
SIGNAL \Wrong|present_state.err_state1~q\ : std_logic;
SIGNAL \Wrong|present_state~8_combout\ : std_logic;
SIGNAL \Wrong|present_state.err_state2~q\ : std_logic;
SIGNAL \Wrong|err_count\ : std_logic_vector(1 DOWNTO 0);
SIGNAL \fsm|ALT_INV_lock~0_combout\ : std_logic;

COMPONENT hard_block
    PORT (
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic);
END COMPONENT;

BEGIN

ww_clk <= clk;
ww_reset <= reset;
ww_code <= code;
ww_enter <= enter;
err_count <= ww_err_count;
lock <= ww_lock;
lock0 <= ww_lock0;
ww_devoe <= devoe;
ww_devclrn <= devclrn;
ww_devpor <= devpor;

\~QUARTUS_CREATED_ADC1~_CHSEL_bus\ <= (\~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\);

\~QUARTUS_CREATED_ADC2~_CHSEL_bus\ <= (\~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\);

\clk~inputclkctrl_INCLK_bus\ <= (vcc & vcc & vcc & \clk~input_o\);
\fsm|ALT_INV_lock~0_combout\ <= NOT \fsm|lock~0_combout\;
auto_generated_inst : hard_block
PORT MAP (
	devoe => ww_devoe,
	devclrn => ww_devclrn,
	devpor => ww_devpor);

-- Location: LCCOMB_X44_Y52_N4
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

-- Location: IOOBUF_X0_Y16_N16
\err_count[0]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \Wrong|err_count\(0),
	devoe => ww_devoe,
	o => \err_count[0]~output_o\);

-- Location: IOOBUF_X0_Y16_N9
\err_count[1]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \Wrong|err_count\(1),
	devoe => ww_devoe,
	o => \err_count[1]~output_o\);

-- Location: IOOBUF_X0_Y18_N9
\lock~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \fsm|lock~0_combout\,
	devoe => ww_devoe,
	o => \lock~output_o\);

-- Location: IOOBUF_X0_Y18_N23
\lock0~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \fsm|ALT_INV_lock~0_combout\,
	devoe => ww_devoe,
	o => \lock0~output_o\);

-- Location: IOIBUF_X0_Y18_N15
\clk~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_clk,
	o => \clk~input_o\);

-- Location: CLKCTRL_G3
\clk~inputclkctrl\ : fiftyfivenm_clkctrl
-- pragma translate_off
GENERIC MAP (
	clock_type => "global clock",
	ena_register_mode => "none")
-- pragma translate_on
PORT MAP (
	inclk => \clk~inputclkctrl_INCLK_bus\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	outclk => \clk~inputclkctrl_outclk\);

-- Location: IOIBUF_X0_Y13_N8
\code[3]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_code(3),
	o => \code[3]~input_o\);

-- Location: IOIBUF_X0_Y13_N15
\code[0]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_code(0),
	o => \code[0]~input_o\);

-- Location: IOIBUF_X0_Y13_N1
\code[1]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_code(1),
	o => \code[1]~input_o\);

-- Location: IOIBUF_X0_Y13_N22
\code[2]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_code(2),
	o => \code[2]~input_o\);

-- Location: LCCOMB_X1_Y13_N0
\fsm|Equal3~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \fsm|Equal3~0_combout\ = (\code[3]~input_o\ & (!\code[0]~input_o\ & (\code[1]~input_o\ & \code[2]~input_o\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0010000000000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \code[3]~input_o\,
	datab => \code[0]~input_o\,
	datac => \code[1]~input_o\,
	datad => \code[2]~input_o\,
	combout => \fsm|Equal3~0_combout\);

-- Location: IOIBUF_X0_Y16_N22
\reset~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_reset,
	o => \reset~input_o\);

-- Location: IOIBUF_X0_Y18_N1
\enter~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_enter,
	o => \enter~input_o\);

-- Location: LCCOMB_X1_Y18_N30
\synchronizer|sync1:resync[1]~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \synchronizer|sync1:resync[1]~0_combout\ = !\enter~input_o\

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0000000011111111",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datad => \enter~input_o\,
	combout => \synchronizer|sync1:resync[1]~0_combout\);

-- Location: FF_X1_Y18_N31
\synchronizer|sync1:resync[1]\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~inputclkctrl_outclk\,
	d => \synchronizer|sync1:resync[1]~0_combout\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \synchronizer|sync1:resync[1]~q\);

-- Location: LCCOMB_X1_Y18_N26
\synchronizer|sync1:resync[2]~feeder\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \synchronizer|sync1:resync[2]~feeder_combout\ = \synchronizer|sync1:resync[1]~q\

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111111100000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datad => \synchronizer|sync1:resync[1]~q\,
	combout => \synchronizer|sync1:resync[2]~feeder_combout\);

-- Location: FF_X1_Y18_N27
\synchronizer|sync1:resync[2]\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~inputclkctrl_outclk\,
	d => \synchronizer|sync1:resync[2]~feeder_combout\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \synchronizer|sync1:resync[2]~q\);

-- Location: LCCOMB_X1_Y18_N28
\synchronizer|sync1:resync[3]~feeder\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \synchronizer|sync1:resync[3]~feeder_combout\ = \synchronizer|sync1:resync[2]~q\

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111000011110000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datac => \synchronizer|sync1:resync[2]~q\,
	combout => \synchronizer|sync1:resync[3]~feeder_combout\);

-- Location: FF_X1_Y18_N29
\synchronizer|sync1:resync[3]\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~inputclkctrl_outclk\,
	d => \synchronizer|sync1:resync[3]~feeder_combout\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \synchronizer|sync1:resync[3]~q\);

-- Location: LCCOMB_X1_Y18_N22
\synchronizer|fall~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \synchronizer|fall~0_combout\ = (!\synchronizer|sync1:resync[2]~q\ & \synchronizer|sync1:resync[3]~q\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0000111100000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datac => \synchronizer|sync1:resync[2]~q\,
	datad => \synchronizer|sync1:resync[3]~q\,
	combout => \synchronizer|fall~0_combout\);

-- Location: FF_X1_Y18_N23
\synchronizer|fall\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~input_o\,
	d => \synchronizer|fall~0_combout\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \synchronizer|fall~q\);

-- Location: LCCOMB_X2_Y18_N12
\fsm|present_state~14\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \fsm|present_state~14_combout\ = (!\synchronizer|fall~q\ & (\reset~input_o\ & \fsm|present_state.get_code2~q\))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0011000000000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datab => \synchronizer|fall~q\,
	datac => \reset~input_o\,
	datad => \fsm|present_state.get_code2~q\,
	combout => \fsm|present_state~14_combout\);

-- Location: LCCOMB_X1_Y13_N22
\fsm|Equal1~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \fsm|Equal1~0_combout\ = (\code[3]~input_o\ & (!\code[0]~input_o\ & (!\code[1]~input_o\ & \code[2]~input_o\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0000001000000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \code[3]~input_o\,
	datab => \code[0]~input_o\,
	datac => \code[1]~input_o\,
	datad => \code[2]~input_o\,
	combout => \fsm|Equal1~0_combout\);

-- Location: LCCOMB_X2_Y18_N8
\fsm|present_state~20\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \fsm|present_state~20_combout\ = (\fsm|Equal3~0_combout\ & (!\fsm|Equal1~0_combout\ & (\fsm|present_state.Ev_code1~q\))) # (!\fsm|Equal3~0_combout\ & ((\fsm|present_state.Ev_code2~q\) # ((!\fsm|Equal1~0_combout\ & \fsm|present_state.Ev_code1~q\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0111010100110000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \fsm|Equal3~0_combout\,
	datab => \fsm|Equal1~0_combout\,
	datac => \fsm|present_state.Ev_code1~q\,
	datad => \fsm|present_state.Ev_code2~q\,
	combout => \fsm|present_state~20_combout\);

-- Location: LCCOMB_X2_Y18_N18
\fsm|present_state~21\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \fsm|present_state~21_combout\ = (\reset~input_o\ & (\fsm|present_state~20_combout\ & ((\fsm|present_state.Ev_code2~q\) # (\fsm|present_state.Ev_code1~q\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1100000010000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \fsm|present_state.Ev_code2~q\,
	datab => \reset~input_o\,
	datac => \fsm|present_state~20_combout\,
	datad => \fsm|present_state.Ev_code1~q\,
	combout => \fsm|present_state~21_combout\);

-- Location: FF_X2_Y18_N19
\fsm|present_state.wrong_code\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~inputclkctrl_outclk\,
	d => \fsm|present_state~21_combout\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \fsm|present_state.wrong_code~q\);

-- Location: LCCOMB_X2_Y18_N4
\fsm|present_state~16\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \fsm|present_state~16_combout\ = (\synchronizer|fall~q\ & ((\fsm|present_state.Unlocked~q\) # ((!\Wrong|present_state.err_state2~q\ & \fsm|present_state.wrong_code~q\)))) # (!\synchronizer|fall~q\ & (!\Wrong|present_state.err_state2~q\ & 
-- ((\fsm|present_state.wrong_code~q\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1011001110100000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \synchronizer|fall~q\,
	datab => \Wrong|present_state.err_state2~q\,
	datac => \fsm|present_state.Unlocked~q\,
	datad => \fsm|present_state.wrong_code~q\,
	combout => \fsm|present_state~16_combout\);

-- Location: LCCOMB_X2_Y18_N20
\fsm|present_state~17\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \fsm|present_state~17_combout\ = (!\fsm|present_state~16_combout\ & (\reset~input_o\ & ((\synchronizer|fall~q\) # (\fsm|present_state.idle~q\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0011001000000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \synchronizer|fall~q\,
	datab => \fsm|present_state~16_combout\,
	datac => \fsm|present_state.idle~q\,
	datad => \reset~input_o\,
	combout => \fsm|present_state~17_combout\);

-- Location: FF_X2_Y18_N21
\fsm|present_state.idle\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~inputclkctrl_outclk\,
	d => \fsm|present_state~17_combout\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \fsm|present_state.idle~q\);

-- Location: LCCOMB_X2_Y18_N6
\fsm|present_state~15\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \fsm|present_state~15_combout\ = (\synchronizer|fall~q\ & (\reset~input_o\ & !\fsm|present_state.idle~q\))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0000000011000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datab => \synchronizer|fall~q\,
	datac => \reset~input_o\,
	datad => \fsm|present_state.idle~q\,
	combout => \fsm|present_state~15_combout\);

-- Location: FF_X2_Y18_N9
\fsm|present_state.Ev_code1\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~inputclkctrl_outclk\,
	asdata => \fsm|present_state~15_combout\,
	sload => VCC,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \fsm|present_state.Ev_code1~q\);

-- Location: LCCOMB_X2_Y18_N28
\fsm|present_state~19\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \fsm|present_state~19_combout\ = (\fsm|present_state~14_combout\) # ((\fsm|Equal1~0_combout\ & (\reset~input_o\ & \fsm|present_state.Ev_code1~q\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1110101010101010",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \fsm|present_state~14_combout\,
	datab => \fsm|Equal1~0_combout\,
	datac => \reset~input_o\,
	datad => \fsm|present_state.Ev_code1~q\,
	combout => \fsm|present_state~19_combout\);

-- Location: FF_X2_Y18_N29
\fsm|present_state.get_code2\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~inputclkctrl_outclk\,
	d => \fsm|present_state~19_combout\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \fsm|present_state.get_code2~q\);

-- Location: LCCOMB_X2_Y18_N24
\fsm|present_state~13\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \fsm|present_state~13_combout\ = (\synchronizer|fall~q\ & (\reset~input_o\ & \fsm|present_state.get_code2~q\))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1100000000000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datab => \synchronizer|fall~q\,
	datac => \reset~input_o\,
	datad => \fsm|present_state.get_code2~q\,
	combout => \fsm|present_state~13_combout\);

-- Location: FF_X2_Y18_N11
\fsm|present_state.Ev_code2\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~inputclkctrl_outclk\,
	asdata => \fsm|present_state~13_combout\,
	sload => VCC,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \fsm|present_state.Ev_code2~q\);

-- Location: LCCOMB_X2_Y18_N16
\fsm|lock~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \fsm|lock~0_combout\ = (\synchronizer|fall~q\) # (!\fsm|present_state.Unlocked~q\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111111100110011",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datab => \fsm|present_state.Unlocked~q\,
	datad => \synchronizer|fall~q\,
	combout => \fsm|lock~0_combout\);

-- Location: LCCOMB_X2_Y18_N10
\fsm|present_state~18\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \fsm|present_state~18_combout\ = (\reset~input_o\ & (((\fsm|Equal3~0_combout\ & \fsm|present_state.Ev_code2~q\)) # (!\fsm|lock~0_combout\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1000000011001100",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \fsm|Equal3~0_combout\,
	datab => \reset~input_o\,
	datac => \fsm|present_state.Ev_code2~q\,
	datad => \fsm|lock~0_combout\,
	combout => \fsm|present_state~18_combout\);

-- Location: FF_X2_Y18_N31
\fsm|present_state.Unlocked\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~inputclkctrl_outclk\,
	asdata => \fsm|present_state~18_combout\,
	sload => VCC,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \fsm|present_state.Unlocked~q\);

-- Location: LCCOMB_X2_Y18_N14
\fsm|Selector0~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \fsm|Selector0~0_combout\ = (!\synchronizer|fall~q\) # (!\fsm|present_state.Unlocked~q\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0000111111111111",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datac => \fsm|present_state.Unlocked~q\,
	datad => \synchronizer|fall~q\,
	combout => \fsm|Selector0~0_combout\);

-- Location: LCCOMB_X2_Y18_N26
\fsm|err_event\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \fsm|err_event~combout\ = (\fsm|Selector0~0_combout\ & ((\fsm|present_state.wrong_code~q\))) # (!\fsm|Selector0~0_combout\ & (\fsm|err_event~combout\))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111101000001010",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \fsm|err_event~combout\,
	datac => \fsm|Selector0~0_combout\,
	datad => \fsm|present_state.wrong_code~q\,
	combout => \fsm|err_event~combout\);

-- Location: LCCOMB_X2_Y18_N30
\Wrong|present_state~7\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Wrong|present_state~7_combout\ = (\fsm|err_event~combout\) # (!\reset~input_o\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111111100110011",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datab => \reset~input_o\,
	datad => \fsm|err_event~combout\,
	combout => \Wrong|present_state~7_combout\);

-- Location: FF_X2_Y18_N1
\Wrong|present_state.idle\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~inputclkctrl_outclk\,
	asdata => \reset~input_o\,
	sload => VCC,
	ena => \Wrong|present_state~7_combout\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \Wrong|present_state.idle~q\);

-- Location: LCCOMB_X2_Y18_N22
\Wrong|present_state~6\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Wrong|present_state~6_combout\ = (\reset~input_o\ & !\Wrong|present_state.idle~q\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0000000011110000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datac => \reset~input_o\,
	datad => \Wrong|present_state.idle~q\,
	combout => \Wrong|present_state~6_combout\);

-- Location: FF_X2_Y18_N23
\Wrong|present_state.err_state0\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~inputclkctrl_outclk\,
	d => \Wrong|present_state~6_combout\,
	ena => \Wrong|present_state~7_combout\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \Wrong|present_state.err_state0~q\);

-- Location: LCCOMB_X2_Y18_N2
\Wrong|present_state~9\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Wrong|present_state~9_combout\ = (\reset~input_o\ & \Wrong|present_state.err_state0~q\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1100000011000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datab => \reset~input_o\,
	datac => \Wrong|present_state.err_state0~q\,
	combout => \Wrong|present_state~9_combout\);

-- Location: FF_X2_Y18_N3
\Wrong|present_state.err_state1\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~inputclkctrl_outclk\,
	d => \Wrong|present_state~9_combout\,
	ena => \Wrong|present_state~7_combout\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \Wrong|present_state.err_state1~q\);

-- Location: LCCOMB_X2_Y18_N0
\Wrong|present_state~8\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Wrong|present_state~8_combout\ = (\reset~input_o\ & ((\Wrong|present_state.err_state2~q\) # ((\fsm|err_event~combout\ & \Wrong|present_state.err_state1~q\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1110000011000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \fsm|err_event~combout\,
	datab => \Wrong|present_state.err_state2~q\,
	datac => \reset~input_o\,
	datad => \Wrong|present_state.err_state1~q\,
	combout => \Wrong|present_state~8_combout\);

-- Location: FF_X2_Y18_N17
\Wrong|present_state.err_state2\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~inputclkctrl_outclk\,
	asdata => \Wrong|present_state~8_combout\,
	sload => VCC,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \Wrong|present_state.err_state2~q\);

-- Location: LCCOMB_X1_Y16_N16
\Wrong|err_count[0]\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Wrong|err_count\(0) = (\Wrong|present_state.err_state2~q\) # (\Wrong|present_state.err_state0~q\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111111110101010",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \Wrong|present_state.err_state2~q\,
	datad => \Wrong|present_state.err_state0~q\,
	combout => \Wrong|err_count\(0));

-- Location: LCCOMB_X1_Y16_N14
\Wrong|err_count[1]\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Wrong|err_count\(1) = (\Wrong|present_state.err_state2~q\) # (\Wrong|present_state.err_state1~q\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111111110101010",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \Wrong|present_state.err_state2~q\,
	datad => \Wrong|present_state.err_state1~q\,
	combout => \Wrong|err_count\(1));

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

ww_err_count(0) <= \err_count[0]~output_o\;

ww_err_count(1) <= \err_count[1]~output_o\;

ww_lock <= \lock~output_o\;

ww_lock0 <= \lock0~output_o\;
END structure;


