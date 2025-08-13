LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.ALL;

ENTITY two_player_guess_game IS

	PORT (
		-- Input ports
		show : IN STD_LOGIC;
		set : IN STD_LOGIC;
		tal : IN STD_LOGIC_VECTOR(7 DOWNTO 0);
		try : IN STD_LOGIC;
		player : IN STD_LOGIC;

		-- Output ports
		hex1 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		hex10 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		hex_p : OUT STD_LOGIC_VECTOR(6 DOWNTO 0)
	);
END two_player_guess_game;

ARCHITECTURE two_player OF two_player_guess_game IS
	SIGNAL show0, show1, set0, set1, try0, try1 : STD_LOGIC;
	SIGNAL input0, input1 : STD_LOGIC_VECTOR(7 DOWNTO 0);
	SIGNAL sseg0, sseg1, yt : STD_LOGIC_VECTOR(13 DOWNTO 0);

BEGIN
	guess_game0 : ENTITY work.guess_game
		PORT MAP
		(
			show => show0,
			set => set0,
			input => input0,
			try => try0,
			hex1 => sseg0(6 DOWNTO 0),
			hex10 => sseg0(13 DOWNTO 7)
		);
	guess_game1 : ENTITY work.guess_game
		PORT MAP
		(
			show => show1,
			set => set1,
			input => input1,
			try => try1,
			hex1 => sseg1(6 DOWNTO 0),
			hex10 => sseg1(13 DOWNTO 7)
		);
	bin2hex : ENTITY work.bin2hex

		PORT MAP
		(
			bin(0) => player,
			seg => hex_p
		);

	mux1 : ENTITY work.mux_in

		PORT MAP
		(
			show => show,
			try => try,
			set => set,
			tal => tal,
			player => player,

			show0_out => show0,
			set0_out => set0,
			out0 => input0,
			try0 => try0,

			show1_out => show1,
			set1_out => set1,
			out1 => input1,
			try1 => try1

		);
	mux2 : ENTITY work.mux_out

		PORT MAP
		(
			sseg0 => sseg0,
			sseg1 => sseg1,
			player => player,
			yt(13 DOWNTO 7) => hex10,
			yt(6 DOWNTO 0) => hex1

		);

END two_player;