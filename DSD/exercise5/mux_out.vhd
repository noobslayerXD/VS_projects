LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;

ENTITY mux_out IS

	PORT (
		-- Input ports
		sseg0 : IN STD_LOGIC_VECTOR(13 DOWNTO 0);
		sseg1 : IN STD_LOGIC_VECTOR(13 DOWNTO 0);
		player : IN STD_LOGIC;

		-- Output ports
		yt : OUT STD_LOGIC_VECTOR(13 DOWNTO 0)

	);
END mux_out;

ARCHITECTURE mux OF mux_out IS
BEGIN
	PROCESS (sseg0, sseg1, player)
	BEGIN
		IF player = '0' THEN
			yt <= sseg0;
		ELSE
			yt <= sseg1;
		END IF;
	END PROCESS;
END mux;