library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use work.all;

entity exercise4_tester is 

	port
	(
		SW: in std_logic_vector(3 downto 0);
		
		HEX0: out std_logic_vector(6 downto 0)
	);
end exercise4_tester;

architecture implementation of exercise4_tester is 

begin

bin2hex : entity work.bin2hex port map (
	bin => SW(3 downto 0),
	seg => HEX0(6 downto 0)
	);
	
end implementation;