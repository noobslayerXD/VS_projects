LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;

ENTITY bin2hex IS

	PORT (
		-- Input ports
		bin : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
		-- Output ports
		seg : OUT STD_LOGIC_VECTOR(6 DOWNTO 0)
	);
END bin2hex;

ARCHITECTURE bin2hex_impl OF bin2hex IS
BEGIN
	PROCESS (bin)
	BEGIN
		CASE bin IS
			WHEN "0000" =>
				seg <= "1000000"; -- Hex: 0
			WHEN "0001" =>
				seg <= "1111001"; -- Hex: 1
			WHEN "0010" =>
				seg <= "0100100"; -- Hex: 2
			WHEN "0011" =>
				seg <= "0110000"; -- Hex: 3
			WHEN "0100" =>
				seg <= "0011001"; -- Hex: 4
			WHEN "0101" =>
				seg <= "0010010"; -- Hex: 5
			WHEN "0110" =>
				seg <= "0000010"; -- Hex: 6
			WHEN "0111" =>
				seg <= "1111000"; -- Hex: 7
			WHEN "1000" =>
				seg <= "0000000"; -- Hex: 8
			WHEN "1001" =>
				seg <= "0010000"; -- Hex: 9
			WHEN "1010" =>
				seg <= "0001000"; -- Hex: A
			WHEN "1011" =>
				seg <= "0000011"; -- Hex: B
			WHEN "1100" =>
				seg <= "1000110"; -- Hex: C
			WHEN "1101" =>
				seg <= "0100001"; -- Hex: D
			WHEN "1110" =>
				seg <= "0000110"; -- Hex: E
			WHEN "1111" =>
				seg <= "0001110"; -- Hex: F
			WHEN OTHERS =>
				seg <= "1111111"; -- All segments off for invalid input
		END CASE;
	END PROCESS;
END bin2hex_impl;