LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;

ENTITY mux2 IS
	PORT (
		-- Input ports
		lo, hi, eq : IN STD_LOGIC;
		seg : IN STD_LOGIC_VECTOR(13 DOWNTO 0);
		-- Output ports
		output : OUT STD_LOGIC_VECTOR(13 DOWNTO 0)
	);
END mux2;

ARCHITECTURE mux2_impl OF mux2 IS
BEGIN
	PROCESS (lo, hi, eq, seg)
	BEGIN
		IF hi = '1' THEN
			output <= "00010011101111";
		END IF;

		IF lo = '1' THEN
			output <= "10001110100011";
		END IF;

		IF eq = '1' THEN
			output <= "01111110111111";
		END IF;
		IF (lo AND hi AND eq) = '0' THEN
			output <= seg;
		END IF;
	END PROCESS;
END mux2_impl;