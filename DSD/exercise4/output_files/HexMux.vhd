library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use work.all;

entity HexMux is
    Port (
       --input
		sel : in STD_LOGIC_VECTOR(1 DOWNTO 0); 
		bin : in std_logic_vector(11 downto 0);
		--output 
      tsseg : out STD_LOGIC_VECTOR(20 DOWNTO 0)
    );
end entity;

ARCHITECTURE behavioral OF HexMux IS
signal hex:std_logic_vector(20 downto 0);
BEGIN
		bin2sevenseg : entity work.exercise4 port map (
			  bin => bin(3 downto 0),
			  Sseg => HEX(6 downto 0)
		 );

		 bin2sevenseg2 : entity work.exercise4 port map (
			  bin => bin(7 downto 4),
			  Sseg => HEX(13 downto 7)
		 );

		 bin2sevenseg3 : entity work.exercise4 port map (
			  bin => bin(11 downto 8),
			  Sseg => HEX(20 downto 14)
		 );

    PROCESS (sel)
    BEGIN
 CASE sel IS
	when "01" =>
		tsseg <= "000011001011110101111";
	when "11" =>
		tsseg <= "111111110000000101011";
	when "10" =>
		tsseg <= hex;
	when others =>
		tsseg <= "111111111111111111111";
END CASE;
END PROCESS;
END behavioral;