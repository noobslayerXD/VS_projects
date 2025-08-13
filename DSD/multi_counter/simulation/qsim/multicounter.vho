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

-- DATE "11/24/2023 19:27:36"

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

ENTITY 	multi_counter IS
    PORT (
	clk : IN std_logic;
	mode : IN std_logic_vector(1 DOWNTO 0);
	reset : IN std_logic;
	clken : IN std_logic;
	count : OUT std_logic_vector(3 DOWNTO 0);
	cout : OUT std_logic
	);
END multi_counter;

-- Design Ports Information
-- count[0]	=>  Location: PIN_A3,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- count[1]	=>  Location: PIN_D5,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- count[2]	=>  Location: PIN_C5,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- count[3]	=>  Location: PIN_B2,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- cout	=>  Location: PIN_B3,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- mode[1]	=>  Location: PIN_C4,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- mode[0]	=>  Location: PIN_F7,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- clk	=>  Location: PIN_M8,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- reset	=>  Location: PIN_M9,	 I/O Standard: 2.5 V,	 Current Strength: Default
-- clken	=>  Location: PIN_E8,	 I/O Standard: 2.5 V,	 Current Strength: Default


ARCHITECTURE structure OF multi_counter IS
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
SIGNAL ww_mode : std_logic_vector(1 DOWNTO 0);
SIGNAL ww_reset : std_logic;
SIGNAL ww_clken : std_logic;
SIGNAL ww_count : std_logic_vector(3 DOWNTO 0);
SIGNAL ww_cout : std_logic;
SIGNAL \~QUARTUS_CREATED_ADC1~_CHSEL_bus\ : std_logic_vector(4 DOWNTO 0);
SIGNAL \~QUARTUS_CREATED_ADC2~_CHSEL_bus\ : std_logic_vector(4 DOWNTO 0);
SIGNAL \reset~inputclkctrl_INCLK_bus\ : std_logic_vector(3 DOWNTO 0);
SIGNAL \clk~inputclkctrl_INCLK_bus\ : std_logic_vector(3 DOWNTO 0);
SIGNAL \~QUARTUS_CREATED_GND~I_combout\ : std_logic;
SIGNAL \~QUARTUS_CREATED_UNVM~~busy\ : std_logic;
SIGNAL \~QUARTUS_CREATED_ADC1~~eoc\ : std_logic;
SIGNAL \~QUARTUS_CREATED_ADC2~~eoc\ : std_logic;
SIGNAL \count[0]~output_o\ : std_logic;
SIGNAL \count[1]~output_o\ : std_logic;
SIGNAL \count[2]~output_o\ : std_logic;
SIGNAL \count[3]~output_o\ : std_logic;
SIGNAL \cout~output_o\ : std_logic;
SIGNAL \clk~input_o\ : std_logic;
SIGNAL \clk~inputclkctrl_outclk\ : std_logic;
SIGNAL \mode[1]~input_o\ : std_logic;
SIGNAL \mode[0]~input_o\ : std_logic;
SIGNAL \Add0~0_combout\ : std_logic;
SIGNAL \counter_proc:cnt[0]~1_combout\ : std_logic;
SIGNAL \Mux1~2_combout\ : std_logic;
SIGNAL \reset~input_o\ : std_logic;
SIGNAL \reset~inputclkctrl_outclk\ : std_logic;
SIGNAL \clken~input_o\ : std_logic;
SIGNAL \counter_proc:cnt[2]~q\ : std_logic;
SIGNAL \Mux0~0_combout\ : std_logic;
SIGNAL \counter_proc:cnt[3]~q\ : std_logic;
SIGNAL \counter_proc:cnt[0]~0_combout\ : std_logic;
SIGNAL \Mux2~2_combout\ : std_logic;
SIGNAL \counter_proc:cnt[1]~q\ : std_logic;
SIGNAL \Mux3~2_combout\ : std_logic;
SIGNAL \counter_proc:cnt[0]~q\ : std_logic;
SIGNAL \cout~1_combout\ : std_logic;
SIGNAL \cout~0_combout\ : std_logic;
SIGNAL \cout~2_combout\ : std_logic;
SIGNAL \cout~reg0_q\ : std_logic;

COMPONENT hard_block
    PORT (
	devoe : IN std_logic;
	devclrn : IN std_logic;
	devpor : IN std_logic);
END COMPONENT;

BEGIN

ww_clk <= clk;
ww_mode <= mode;
ww_reset <= reset;
ww_clken <= clken;
count <= ww_count;
cout <= ww_cout;
ww_devoe <= devoe;
ww_devclrn <= devclrn;
ww_devpor <= devpor;

\~QUARTUS_CREATED_ADC1~_CHSEL_bus\ <= (\~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\);

\~QUARTUS_CREATED_ADC2~_CHSEL_bus\ <= (\~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\ & \~QUARTUS_CREATED_GND~I_combout\);

\reset~inputclkctrl_INCLK_bus\ <= (vcc & vcc & vcc & \reset~input_o\);

\clk~inputclkctrl_INCLK_bus\ <= (vcc & vcc & vcc & \clk~input_o\);
auto_generated_inst : hard_block
PORT MAP (
	devoe => ww_devoe,
	devclrn => ww_devclrn,
	devpor => ww_devpor);

-- Location: LCCOMB_X44_Y49_N12
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

-- Location: IOOBUF_X26_Y39_N9
\count[0]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \counter_proc:cnt[0]~q\,
	devoe => ww_devoe,
	o => \count[0]~output_o\);

-- Location: IOOBUF_X24_Y39_N30
\count[1]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \counter_proc:cnt[1]~q\,
	devoe => ww_devoe,
	o => \count[1]~output_o\);

-- Location: IOOBUF_X24_Y39_N23
\count[2]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \counter_proc:cnt[2]~q\,
	devoe => ww_devoe,
	o => \count[2]~output_o\);

-- Location: IOOBUF_X22_Y39_N16
\count[3]~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \counter_proc:cnt[3]~q\,
	devoe => ww_devoe,
	o => \count[3]~output_o\);

-- Location: IOOBUF_X26_Y39_N16
\cout~output\ : fiftyfivenm_io_obuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	open_drain_output => "false")
-- pragma translate_on
PORT MAP (
	i => \cout~reg0_q\,
	devoe => ww_devoe,
	o => \cout~output_o\);

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

-- Location: IOIBUF_X24_Y39_N1
\mode[1]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_mode(1),
	o => \mode[1]~input_o\);

-- Location: IOIBUF_X24_Y39_N15
\mode[0]~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_mode(0),
	o => \mode[0]~input_o\);

-- Location: LCCOMB_X24_Y38_N10
\Add0~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Add0~0_combout\ = (\counter_proc:cnt[0]~q\ & \counter_proc:cnt[1]~q\)

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1111000000000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	datac => \counter_proc:cnt[0]~q\,
	datad => \counter_proc:cnt[1]~q\,
	combout => \Add0~0_combout\);

-- Location: LCCOMB_X24_Y38_N24
\counter_proc:cnt[0]~1\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \counter_proc:cnt[0]~1_combout\ = (\mode[1]~input_o\ & (!\counter_proc:cnt[0]~q\ & (\counter_proc:cnt[1]~q\ & !\counter_proc:cnt[0]~0_combout\))) # (!\mode[1]~input_o\ & (\counter_proc:cnt[0]~q\ & (!\counter_proc:cnt[1]~q\ & 
-- \counter_proc:cnt[0]~0_combout\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0000010000100000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \mode[1]~input_o\,
	datab => \counter_proc:cnt[0]~q\,
	datac => \counter_proc:cnt[1]~q\,
	datad => \counter_proc:cnt[0]~0_combout\,
	combout => \counter_proc:cnt[0]~1_combout\);

-- Location: LCCOMB_X24_Y38_N16
\Mux1~2\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux1~2_combout\ = (!\counter_proc:cnt[0]~1_combout\ & (\counter_proc:cnt[2]~q\ $ (((\counter_proc:cnt[1]~q\ & \counter_proc:cnt[0]~q\)))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0000000001111000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \counter_proc:cnt[1]~q\,
	datab => \counter_proc:cnt[0]~q\,
	datac => \counter_proc:cnt[2]~q\,
	datad => \counter_proc:cnt[0]~1_combout\,
	combout => \Mux1~2_combout\);

-- Location: IOIBUF_X0_Y18_N22
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

-- Location: CLKCTRL_G4
\reset~inputclkctrl\ : fiftyfivenm_clkctrl
-- pragma translate_off
GENERIC MAP (
	clock_type => "global clock",
	ena_register_mode => "none")
-- pragma translate_on
PORT MAP (
	inclk => \reset~inputclkctrl_INCLK_bus\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	outclk => \reset~inputclkctrl_outclk\);

-- Location: IOIBUF_X24_Y39_N8
\clken~input\ : fiftyfivenm_io_ibuf
-- pragma translate_off
GENERIC MAP (
	bus_hold => "false",
	listen_to_nsleep_signal => "false",
	simulate_z_as => "z")
-- pragma translate_on
PORT MAP (
	i => ww_clken,
	o => \clken~input_o\);

-- Location: FF_X24_Y38_N17
\counter_proc:cnt[2]\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~inputclkctrl_outclk\,
	d => \Mux1~2_combout\,
	clrn => \reset~inputclkctrl_outclk\,
	ena => \clken~input_o\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \counter_proc:cnt[2]~q\);

-- Location: LCCOMB_X24_Y38_N30
\Mux0~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux0~0_combout\ = (!\counter_proc:cnt[0]~1_combout\ & (\counter_proc:cnt[3]~q\ $ (((\Add0~0_combout\ & \counter_proc:cnt[2]~q\)))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0000000001111000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \Add0~0_combout\,
	datab => \counter_proc:cnt[2]~q\,
	datac => \counter_proc:cnt[3]~q\,
	datad => \counter_proc:cnt[0]~1_combout\,
	combout => \Mux0~0_combout\);

-- Location: FF_X24_Y38_N31
\counter_proc:cnt[3]\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~inputclkctrl_outclk\,
	d => \Mux0~0_combout\,
	clrn => \reset~inputclkctrl_outclk\,
	ena => \clken~input_o\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \counter_proc:cnt[3]~q\);

-- Location: LCCOMB_X24_Y38_N6
\counter_proc:cnt[0]~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \counter_proc:cnt[0]~0_combout\ = (\mode[0]~input_o\ & ((\counter_proc:cnt[3]~q\ & (\counter_proc:cnt[1]~q\)) # (!\counter_proc:cnt[3]~q\ & ((\counter_proc:cnt[2]~q\))))) # (!\mode[0]~input_o\ & ((\counter_proc:cnt[2]~q\ & (\counter_proc:cnt[1]~q\)) # 
-- (!\counter_proc:cnt[2]~q\ & ((\counter_proc:cnt[3]~q\)))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "1100111011010000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \mode[0]~input_o\,
	datab => \counter_proc:cnt[1]~q\,
	datac => \counter_proc:cnt[3]~q\,
	datad => \counter_proc:cnt[2]~q\,
	combout => \counter_proc:cnt[0]~0_combout\);

-- Location: LCCOMB_X24_Y38_N18
\Mux2~2\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux2~2_combout\ = (\counter_proc:cnt[0]~q\ & (!\counter_proc:cnt[1]~q\ & ((\mode[1]~input_o\) # (!\counter_proc:cnt[0]~0_combout\)))) # (!\counter_proc:cnt[0]~q\ & (\counter_proc:cnt[1]~q\ & ((\counter_proc:cnt[0]~0_combout\) # (!\mode[1]~input_o\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0101100000011010",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \counter_proc:cnt[0]~q\,
	datab => \mode[1]~input_o\,
	datac => \counter_proc:cnt[1]~q\,
	datad => \counter_proc:cnt[0]~0_combout\,
	combout => \Mux2~2_combout\);

-- Location: FF_X24_Y38_N19
\counter_proc:cnt[1]\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~inputclkctrl_outclk\,
	d => \Mux2~2_combout\,
	clrn => \reset~inputclkctrl_outclk\,
	ena => \clken~input_o\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \counter_proc:cnt[1]~q\);

-- Location: LCCOMB_X24_Y38_N8
\Mux3~2\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \Mux3~2_combout\ = (!\counter_proc:cnt[0]~q\ & (((\counter_proc:cnt[0]~0_combout\) # (!\counter_proc:cnt[1]~q\)) # (!\mode[1]~input_o\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0000111100000111",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \mode[1]~input_o\,
	datab => \counter_proc:cnt[1]~q\,
	datac => \counter_proc:cnt[0]~q\,
	datad => \counter_proc:cnt[0]~0_combout\,
	combout => \Mux3~2_combout\);

-- Location: FF_X24_Y38_N9
\counter_proc:cnt[0]\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~inputclkctrl_outclk\,
	d => \Mux3~2_combout\,
	clrn => \reset~inputclkctrl_outclk\,
	ena => \clken~input_o\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \counter_proc:cnt[0]~q\);

-- Location: LCCOMB_X24_Y38_N26
\cout~1\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \cout~1_combout\ = (\counter_proc:cnt[3]~q\ & (((!\mode[0]~input_o\ & !\counter_proc:cnt[2]~q\)) # (!\counter_proc:cnt[0]~q\))) # (!\counter_proc:cnt[3]~q\ & (\counter_proc:cnt[2]~q\ & ((\mode[0]~input_o\) # (!\counter_proc:cnt[0]~q\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0100111100101010",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \counter_proc:cnt[3]~q\,
	datab => \mode[0]~input_o\,
	datac => \counter_proc:cnt[0]~q\,
	datad => \counter_proc:cnt[2]~q\,
	combout => \cout~1_combout\);

-- Location: LCCOMB_X24_Y38_N20
\cout~0\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \cout~0_combout\ = (\clken~input_o\ & (\mode[1]~input_o\ $ (\counter_proc:cnt[0]~q\)))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0000101010100000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \clken~input_o\,
	datac => \mode[1]~input_o\,
	datad => \counter_proc:cnt[0]~q\,
	combout => \cout~0_combout\);

-- Location: LCCOMB_X24_Y38_N28
\cout~2\ : fiftyfivenm_lcell_comb
-- Equation(s):
-- \cout~2_combout\ = (\cout~0_combout\ & ((\counter_proc:cnt[1]~q\ & (!\counter_proc:cnt[0]~q\ & !\cout~1_combout\)) # (!\counter_proc:cnt[1]~q\ & (\counter_proc:cnt[0]~q\ & \cout~1_combout\))))

-- pragma translate_off
GENERIC MAP (
	lut_mask => "0100001000000000",
	sum_lutc_input => "datac")
-- pragma translate_on
PORT MAP (
	dataa => \counter_proc:cnt[1]~q\,
	datab => \counter_proc:cnt[0]~q\,
	datac => \cout~1_combout\,
	datad => \cout~0_combout\,
	combout => \cout~2_combout\);

-- Location: FF_X24_Y38_N29
\cout~reg0\ : dffeas
-- pragma translate_off
GENERIC MAP (
	is_wysiwyg => "true",
	power_up => "low")
-- pragma translate_on
PORT MAP (
	clk => \clk~inputclkctrl_outclk\,
	d => \cout~2_combout\,
	clrn => \reset~inputclkctrl_outclk\,
	devclrn => ww_devclrn,
	devpor => ww_devpor,
	q => \cout~reg0_q\);

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

ww_count(0) <= \count[0]~output_o\;

ww_count(1) <= \count[1]~output_o\;

ww_count(2) <= \count[2]~output_o\;

ww_count(3) <= \count[3]~output_o\;

ww_cout <= \cout~output_o\;
END structure;


