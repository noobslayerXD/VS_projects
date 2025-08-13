library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.all;

entity full_adder is

	port
	(
		-- Input ports
		A,B,Cin	: in  std_logic;

		-- Output ports
		Sum,Cout	: out std_logic
	);
end full_adder;


architecture full_adder_struct of full_adder is

signal s1, c1, c2: std_logic;

begin

-- each half adder using structual code to implement both.
h1: entity work.half_adder_structural port map (A =>A, B => B, Sum => s1, Cout => c1);
h2: entity work.half_adder_structural port map (A =>s1, B => Cin, Sum => Sum, Cout => c2);

Cout <= c2 OR c1;


end full_adder_struct;



