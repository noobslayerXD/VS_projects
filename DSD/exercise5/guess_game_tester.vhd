LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.ALL;

ENTITY guess_game_tester IS
	PORT (
		-- Input ports
		SW : IN STD_LOGIC_VECTOR(9 DOWNTO 0);
		KEY : IN STD_LOGIC_VECTOR(3 DOWNTO 0);

		-- Output ports
		HEX1 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		HEX0 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0)
	);
END guess_game_tester;
ARCHITECTURE guess_game_tester_impl OF guess_game_tester IS
BEGIN
	one_player : ENTITY work.guess_game

		PORT MAP
		(
			input => SW(7 DOWNTO 0),
			show => KEY(0),
			set => NOT sw(9),
			try => KEY(1),
			hex1 => HEX0,
			hex10 => HEX1
		);
END guess_game_tester_impl;