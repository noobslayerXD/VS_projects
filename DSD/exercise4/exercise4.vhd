library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use work.all;

entity exercise4 is
    Port (
       --input
		bin : in STD_LOGIC_VECTOR(3 DOWNTO 0); 
		--output 
       Sseg : out STD_LOGIC_VECTOR(6 DOWNTO 0)
    );
end entity;

ARCHITECTURE behavioral OF exercise4 IS
BEGIN
    PROCESS (bin)
    BEGIN
 CASE bin IS
	  WHEN "0000" =>
			Sseg <= "1000000"; -- Hex: 0
	  WHEN "0001" =>
			Sseg <= "1111001"; -- Hex: 1
	  WHEN "0010" =>
			Sseg <= "0100100"; -- Hex: 2
	  WHEN "0011" =>
			Sseg <= "0110000"; -- Hex: 3
	  WHEN "0100" =>
			Sseg <= "0011001"; -- Hex: 4
	  WHEN "0101" =>
			Sseg <= "0010010"; -- Hex: 5
	  WHEN "0110" =>
			Sseg <= "0000010"; -- Hex: 6
	  WHEN "0111" =>
			Sseg <= "1111000"; -- Hex: 7
	  WHEN "1000" =>
			Sseg <= "0000000"; -- Hex: 8
	  WHEN "1001" =>
			Sseg <= "0010000"; -- Hex: 9
	  WHEN "1010" =>
			Sseg <= "0001000"; -- Hex: A
	  WHEN "1011" =>
			Sseg <= "0000011"; -- Hex: B
	  WHEN "1100" =>
			Sseg <= "1000110"; -- Hex: C
	  WHEN "1101" =>
			Sseg <= "0100001"; -- Hex: D
	  WHEN "1110" =>
			Sseg <= "0000110"; -- Hex: E
	  WHEN "1111" =>
			Sseg <= "0001110"; -- Hex: F
	  WHEN OTHERS =>
			Sseg <= "1111111"; -- All segments off for invalid input
 END CASE;
END PROCESS;
END behavioral;
