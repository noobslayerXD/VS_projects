LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;

ENTITY mux_in IS

	PORT (
		-- Input ports
		show : IN STD_LOGIC;
		set : IN STD_LOGIC;
		tal : IN STD_LOGIC_VECTOR(7 DOWNTO 0);
		try : IN STD_LOGIC;
		player : IN STD_LOGIC;

		-- Output ports
		show0_out : OUT STD_LOGIC;
		set0_out : OUT STD_LOGIC;
		out0 : OUT STD_LOGIC_VECTOR(7 DOWNTO 0);
		try0 : OUT STD_LOGIC;

		show1_out : OUT STD_LOGIC;
		set1_out : OUT STD_LOGIC;
		out1 : OUT STD_LOGIC_VECTOR(7 DOWNTO 0);
		try1 : OUT STD_LOGIC

	);
END mux_in;

ARCHITECTURE mux OF mux_in IS
BEGIN
	PROCESS (set, show, tal, try, player)
	BEGIN
		IF player = '0' THEN
			show0_out <= show;
			set0_out <= set;
			try0 <= try;
			show1_out <= '1';
			set1_out <= '1';
			try1 <= '1';

		ELSE
			show0_out <= '1';
			set0_out <= '1';
			try0 <= '1';
			show1_out <= show;
			set1_out <= set;
			try1 <= try;
		END IF;
	END PROCESS;

	out0 <= tal;
	out1 <= tal;

END mux;