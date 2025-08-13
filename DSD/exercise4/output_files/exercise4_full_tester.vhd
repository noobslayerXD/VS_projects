library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use work.all;

entity exercise4_full_tester is
    port (
        --inputs
		  SW: in std_logic_vector(11 downto 0);
        KEY: in std_logic_vector(1 downto 0);
		  --outputs
        HEX0: out std_logic_vector(6 downto 0);
        HEX1: out std_logic_vector(6 downto 0);
        HEX2: out std_logic_vector(6 downto 0)
    );
end exercise4_full_tester;


architecture implementation of exercise4_full_tester is
begin
	 	
		
		 sel : entity work.HexMux port map (
			sel => KEY(1 downto 0),
			bin => SW(11 downto 0),
			tsseg (6 downto 0) => HEX0(6 downto 0),
			tsseg (13 downto 7) => HEX1(6 downto 0),
			tsseg (20 downto 14) => HEX2(6 downto 0)
			);
end implementation;
