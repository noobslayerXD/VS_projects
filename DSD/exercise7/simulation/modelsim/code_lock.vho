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

-- DATE "11/27/2023 16:56:52"

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

ENTITY 	code_lock_simple_fsm IS
    PORT (
	reset : IN std_logic;
	enter : IN std_logic;
	code : IN std_logic_vector(3 DOWNTO 0);
	clk : IN std_logic;
	lock : BUFFER std_logic;
	err_event : BUFFER std_logic
	);
END code_lock_simple_fsm;

-- Design Ports Information
-- lock	=>  Location: PIN_V8,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- err_event	=>  Location: PIN_N2,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- reset	=>  Location: PIN_R9,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- clk	=>  Location: PIN_M8,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- code[1]	=>  Location: PIN_AB2,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- code[2]	=>  Location: PIN_W9,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- code[3]	=>  Location: PIN_P9,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- code[0]	=>  Location: PIN_W10,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- enter	=>  Location: PIN_AB3,	 I/O Standard: 2.5 V,	 Current Strength: Default


ARCHITECTURE structure OF code_lock_simple_fsm IS
SIGNAL gnd : std_logic := '0';
SIGNAL vcc : std_logic := '1';
SIGNAL unknown : std_logic := 'X';
SIGNAL devoe : std_logic := '1';
SIGNAL devclrn : std_logic := '1';
SIGNAL devpor : std_logic := '1';
SIGNAL ww_devoe : std_logic;
SIGNAL ww_devclrn : std_logic;
SIGNAL ww_devpor : std_logic;
SIGNAL ww_reset : std_logic;
SIGNAL ww_enter : std_logic;
SIGNAL ww_code : std_logic_vector(3 DOWNTO 0);
SIGNAL ww_clk : std_logic;
SIGNAL ww_lock : std_logic;
SIGNAL ww_err_event : std_logic;
SIGNAL \~QUARTUS_CREATED_ADC1~_CHSEL_bus\ : std_logic_vector(4 DOWNTO 0);
SIGNAL \~QUARTUS_CREATED_ADC2~_CHSEL_bus\ : std_logic_vector(4 DOWNTO 0);
SIGNAL \Selector0~0clkctrl_INCLK_bus\ : std_logic_vector(3 DOWNTO 0);
SIGNAL \clk~inputclkctrl_INCLK_bus\ : std_logic_vector(3 DOWNTO 0);
SIGNAL \~QUARTUS_CREATED_GND~I_combout\ : std_logic;
SIGNAL \~QUARTUS_CREATED_UNVM~~busy\ : std_logic;
SIGNAL \~QUARTUS_CREATED_ADC1~~eoc\ : std_logic;
SIGNAL \~QUARTUS_CREATED_ADC2~~eoc\ : std_logic;
SIGNAL \lock~output_o\ : std_logic;
SIGNAL \err_event~output_o\ : std_logic;
SIGNAL \clk~input_o\ : std_logic;
SIGNAL \reset~input_o\ : std_logic;
SIGNAL \code[1]~input_o\ : std_logic;
SIGNAL \code[3]~input_o\ : std_logic;
SIGNAL \code[2]~input_o\ : std_logic;
SIGNAL \code[0]~input_o\ : std_logic;
SIGNAL \Selector8~0_combout\ : std_logic;
SIGNAL \clk~inputclkctrl_outclk\ : std_logic;
SIGNAL \next_state.Ev_code1_341~combout\ : std_logic;
SIGNAL \present_state~13_combout\ : std_logic;
SIGNAL \present_state.Ev_code1~q\ : std_logic;
SIGNAL \Selector1~0_combout\ : std_logic;
SIGNAL \Selector1~1_combout\ : std_logic;
SIGNAL \next_state.idle_352~combout\ : std_logic;
SIGNAL \present_state~11_combout\ : std_logic;
SIGNAL \present_state.idle~q\ : std_logic;
SIGNAL \enter~input_o\ : std_logic;
SIGNAL \Selector5~0_combout\ : std_logic;
SIGNAL \next_state.get_code2_330~combout\ : std_logic;
SIGNAL \present_state~12_combout\ : std_logic;
SIGNAL \present_state.get_code2~q\ : std_logic;
SIGNAL \Selector0~0_combout\ : std_logic;
SIGNAL \Selector0~0clkctrl_outclk\ : std_logic;
SIGNAL \next_state.Ev_code2_319~combout\ : std_logic;
SIGNAL \present_state~10_combout\ : std_logic;
SIGNAL \present_state.Ev_code2~q\ : std_logic;
SIGNAL \Selector8~1_combout\ : std_logic;
SIGNAL \next_state.Unlocked_308~combout\ : std_logic;
SIGNAL \present_state~9_combout\ : std_logic;
SIGNAL \present_state.Unlocked~q\ : std_logic;
SIGNAL \ALT_INV_present_state.Unlocked~q\ : std_logic;

COMPONENT hard_block
    PORT (
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic);
END COMPONENT;

BEGIN

ww_reset <= reset;
ww_enter <= enter;
ww_code <= code;
ww_clk <= clk;
lock <= ww_lock;
err_event <= ww_err_event;
ww_devoe <= devoe;
ww_devclrn <= devclrn;
ww_devpor <= devpor;

\~QUARTUS_CREATED_ADC1~_CHSEL_bus\ <= (\~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\);

\~QUARTUS_CREATED_ADC2~_CHSEL_bus\ <= (\~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\);

\Selector0~0clkctrl_INCLK_bus\ <= (vcc & vcc & vcc & \Selector0~0_combout\);

\clk~inputclkctrl_INCLK_bus\ <= (vcc & vcc & vcc & \clk~input_o\);
\ALT_INV_present_state.Unlocked~q\ <= NOT \present_state.Unlocked~q\;
auto_generated_inst : hard_block
PORT MAP (
	devoe => ww_devoe,
	devclrn => ww_devclrn,
	devpor => ww_devpor);

-- Location: LCCOMB_X44_Y41_N24
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

-- Location: IOOBUF_X20_Y0_N16
\lock~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \ALT_INV_present_state.Unlocked~q\,
	devoe => ww_devoe,
	o => \lock~output_o\);

-- Location: IOOBUF_X0_Y18_N9
\err_event~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => VCC,
	devoe => ww_devoe,
	o => \err_event~output_o\);

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

-- Location: IOIBUF_X22_Y0_N29
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

-- Location: IOIBUF_X22_Y0_N15
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

-- Location: IOIBUF_X22_Y0_N22
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

-- Location: IOIBUF_X22_Y0_N1
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

-- Location: IOIBUF_X24_Y0_N29
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

-- Location: LCCOMB_X22_Y4_N30
\Selector8~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Selector8~0_combout\ = (\code[3]~input_o\ & (\code[2]~input_o\ & !\code[0]~input_o\))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0000000011000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datab => \code[3]~input_o\,
	datac => \code[2]~input_o\,
	datad => \code[0]~input_o\,
	combout => \Selector8~0_combout\);

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

-- Location: LCCOMB_X22_Y4_N2
\next_state.Ev_code1_341\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \next_state.Ev_code1_341~combout\ = (GLOBAL(\Selector0~0clkctrl_outclk\) & ((!\present_state.idle~q\))) # (!GLOBAL(\Selector0~0clkctrl_outclk\) & (\next_state.Ev_code1_341~combout\))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0000111111001100",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datab => \next_state.Ev_code1_341~combout\,
	datac => \present_state.idle~q\,
	datad => \Selector0~0clkctrl_outclk\,
	combout => \next_state.Ev_code1_341~combout\);

-- Location: LCCOMB_X22_Y4_N22
\present_state~13\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \present_state~13_combout\ = (\reset~input_o\ & \next_state.Ev_code1_341~combout\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111000000000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datac => \reset~input_o\,
	datad => \next_state.Ev_code1_341~combout\,
	combout => \present_state~13_combout\);

-- Location: FF_X22_Y4_N23
\present_state.Ev_code1\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~inputclkctrl_outclk\,
	d => \present_state~13_combout\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \present_state.Ev_code1~q\);

-- Location: LCCOMB_X22_Y4_N8
\Selector1~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Selector1~0_combout\ = (\present_state.Unlocked~q\) # ((\code[1]~input_o\ & ((\present_state.Ev_code1~q\))) # (!\code[1]~input_o\ & (\present_state.Ev_code2~q\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111101011101110",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \present_state.Unlocked~q\,
	datab => \present_state.Ev_code2~q\,
	datac => \present_state.Ev_code1~q\,
	datad => \code[1]~input_o\,
	combout => \Selector1~0_combout\);

-- Location: LCCOMB_X22_Y4_N20
\Selector1~1\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Selector1~1_combout\ = (\Selector1~0_combout\) # ((!\Selector8~0_combout\ & ((\present_state.Ev_code2~q\) # (\present_state.Ev_code1~q\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1101110111011100",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \Selector8~0_combout\,
	datab => \Selector1~0_combout\,
	datac => \present_state.Ev_code2~q\,
	datad => \present_state.Ev_code1~q\,
	combout => \Selector1~1_combout\);

-- Location: LCCOMB_X22_Y4_N24
\next_state.idle_352\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \next_state.idle_352~combout\ = (GLOBAL(\Selector0~0clkctrl_outclk\) & (\Selector1~1_combout\)) # (!GLOBAL(\Selector0~0clkctrl_outclk\) & ((\next_state.idle_352~combout\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1100110011110000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datab => \Selector1~1_combout\,
	datac => \next_state.idle_352~combout\,
	datad => \Selector0~0clkctrl_outclk\,
	combout => \next_state.idle_352~combout\);

-- Location: LCCOMB_X22_Y4_N10
\present_state~11\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \present_state~11_combout\ = (\reset~input_o\ & !\next_state.idle_352~combout\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0000000011110000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datac => \reset~input_o\,
	datad => \next_state.idle_352~combout\,
	combout => \present_state~11_combout\);

-- Location: FF_X22_Y4_N11
\present_state.idle\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~input_o\,
	d => \present_state~11_combout\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \present_state.idle~q\);

-- Location: IOIBUF_X22_Y0_N8
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

-- Location: LCCOMB_X22_Y4_N0
\Selector5~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Selector5~0_combout\ = (!\code[1]~input_o\ & (\present_state.Ev_code1~q\ & \Selector8~0_combout\))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0100000001000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \code[1]~input_o\,
	datab => \present_state.Ev_code1~q\,
	datac => \Selector8~0_combout\,
	combout => \Selector5~0_combout\);

-- Location: LCCOMB_X22_Y4_N12
\next_state.get_code2_330\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \next_state.get_code2_330~combout\ = (GLOBAL(\Selector0~0clkctrl_outclk\) & ((\Selector5~0_combout\))) # (!GLOBAL(\Selector0~0clkctrl_outclk\) & (\next_state.get_code2_330~combout\))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1100110010101010",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \next_state.get_code2_330~combout\,
	datab => \Selector5~0_combout\,
	datad => \Selector0~0clkctrl_outclk\,
	combout => \next_state.get_code2_330~combout\);

-- Location: LCCOMB_X22_Y4_N14
\present_state~12\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \present_state~12_combout\ = (\reset~input_o\ & \next_state.get_code2_330~combout\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111000000000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datac => \reset~input_o\,
	datad => \next_state.get_code2_330~combout\,
	combout => \present_state~12_combout\);

-- Location: FF_X22_Y4_N15
\present_state.get_code2\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~input_o\,
	d => \present_state~12_combout\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \present_state.get_code2~q\);

-- Location: LCCOMB_X22_Y4_N4
\Selector0~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Selector0~0_combout\ = (\enter~input_o\) # ((\present_state.idle~q\ & (!\present_state.get_code2~q\ & !\present_state.Unlocked~q\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1100110011001110",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \present_state.idle~q\,
	datab => \enter~input_o\,
	datac => \present_state.get_code2~q\,
	datad => \present_state.Unlocked~q\,
	combout => \Selector0~0_combout\);

-- Location: CLKCTRL_G16
\Selector0~0clkctrl\ : fiftyfivenm_clkctrl
-- pragma translate_off
GENERIC MAP (
	clock_type => "global clock",
	ena_register_mode => "none")
-- pragma translate_on
PORT MAP (
	inclk => \Selector0~0clkctrl_INCLK_bus\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	outclk => \Selector0~0clkctrl_outclk\);

-- Location: LCCOMB_X22_Y4_N18
\next_state.Ev_code2_319\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \next_state.Ev_code2_319~combout\ = (GLOBAL(\Selector0~0clkctrl_outclk\) & ((\present_state.get_code2~q\))) # (!GLOBAL(\Selector0~0clkctrl_outclk\) & (\next_state.Ev_code2_319~combout\))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111110000001100",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datab => \next_state.Ev_code2_319~combout\,
	datac => \Selector0~0clkctrl_outclk\,
	datad => \present_state.get_code2~q\,
	combout => \next_state.Ev_code2_319~combout\);

-- Location: LCCOMB_X22_Y4_N26
\present_state~10\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \present_state~10_combout\ = (\reset~input_o\ & \next_state.Ev_code2_319~combout\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111000000000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datac => \reset~input_o\,
	datad => \next_state.Ev_code2_319~combout\,
	combout => \present_state~10_combout\);

-- Location: FF_X22_Y4_N27
\present_state.Ev_code2\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~inputclkctrl_outclk\,
	d => \present_state~10_combout\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \present_state.Ev_code2~q\);

-- Location: LCCOMB_X22_Y4_N28
\Selector8~1\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Selector8~1_combout\ = (\code[1]~input_o\ & (\Selector8~0_combout\ & \present_state.Ev_code2~q\))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1010000000000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \code[1]~input_o\,
	datac => \Selector8~0_combout\,
	datad => \present_state.Ev_code2~q\,
	combout => \Selector8~1_combout\);

-- Location: LCCOMB_X22_Y4_N16
\next_state.Unlocked_308\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \next_state.Unlocked_308~combout\ = (GLOBAL(\Selector0~0clkctrl_outclk\) & (\Selector8~1_combout\)) # (!GLOBAL(\Selector0~0clkctrl_outclk\) & ((\next_state.Unlocked_308~combout\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1100110011110000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datab => \Selector8~1_combout\,
	datac => \next_state.Unlocked_308~combout\,
	datad => \Selector0~0clkctrl_outclk\,
	combout => \next_state.Unlocked_308~combout\);

-- Location: LCCOMB_X22_Y4_N6
\present_state~9\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \present_state~9_combout\ = (\reset~input_o\ & \next_state.Unlocked_308~combout\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111000000000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datac => \reset~input_o\,
	datad => \next_state.Unlocked_308~combout\,
	combout => \present_state~9_combout\);

-- Location: FF_X22_Y4_N7
\present_state.Unlocked\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~input_o\,
	d => \present_state~9_combout\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \present_state.Unlocked~q\);

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

ww_lock <= \lock~output_o\;

ww_err_event <= \err_event~output_o\;
END structure;


