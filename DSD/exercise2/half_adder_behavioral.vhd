library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.all;

entity half_adder_behavioral is

	port (
		-- Input ports
		A : in std_logic;
		B : in std_logic;

		-- Output ports
		Sum : out std_logic;
		Cout : out std_logic
	);
end half_adder_behavioral;

architecture half_adder_behavioral of half_adder_behavioral is
begin
	Sum <= '1' when (A ='1' XOR B = '1') 
		else '0';
			
	Cout <= '1' when (A = '1' AND B = '1')
				else '0';

end half_adder_behavioral;



