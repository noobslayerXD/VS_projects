LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.ALL;

ENTITY guess_game IS
	PORT (
		-- Input ports
		show : IN STD_LOGIC; --Show predefined value
		set : IN STD_LOGIC; --Set predefined value
		input : IN STD_LOGIC_VECTOR(7 DOWNTO 0);
		try : IN STD_LOGIC; --Evaluate guess
		-- Output ports
		hex1 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		hex10 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0)
	);
END guess_game;
ARCHITECTURE guess_game_impl OF guess_game IS
	--interne signaler
	SIGNAL secret_value : STD_LOGIC_VECTOR(7 DOWNTO 0);
	SIGNAL mux2bin : STD_LOGIC_VECTOR(7 DOWNTO 0);
	SIGNAL hex2mux : STD_LOGIC_VECTOR(13 DOWNTO 0);
	SIGNAL hex2disp : STD_LOGIC_VECTOR(13 DOWNTO 0);
	SIGNAL lo : STD_LOGIC;
	SIGNAL hi : STD_LOGIC;
	SIGNAL eq : STD_LOGIC;

BEGIN
	Latch : ENTITY work.mylatch

		PORT MAP
		(
			set => set,
			input => input,
			set_val => secret_value
		);
	Compare_logic : ENTITY work.compare

		PORT MAP
		(
			set_val => secret_value,
			try_val => input,
			try => try
		);
	Mux1 : ENTITY work.mux1

		PORT MAP
		(
			show => show,
			set_val => secret_value,
			try_val => input,
			mux1_out => mux2bin
		);
	bin2hex1 : ENTITY work.bin2hex

		PORT MAP
		(
			bin => mux2bin(3 DOWNTO 0),
			seg => hex2mux(6 DOWNTO 0)
		);

	bin2hex2 : ENTITY work.bin2hex
		PORT MAP
		(
			bin => mux2bin(7 DOWNTO 4),
			seg => hex2mux(13 DOWNTO 7)
		);

	--- Her instantieres Mux2
	mux2 : ENTITY work.mux2
		PORT MAP
		(
			lo => lo,
			hi => hi,
			eq => eq,
			seg => hex2mux,
			output => hex2disp
		);

	hex1 <= hex2disp(6 DOWNTO 0);
	hex10 <= hex2disp(13 DOWNTO 7);

END guess_game_impl;