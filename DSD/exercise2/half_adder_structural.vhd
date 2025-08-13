library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.all;

entity half_adder_structural is

	port (
		-- Input ports
		A : in std_logic;
		B : in std_logic;

		-- Output ports
		Sum : out std_logic;
		Cout : out std_logic
	);
end half_adder_structural;



architecture half_adder_structural of half_adder_structural is

	-- Declarations (optional)

begin
u1: entity work.my_and port map (a =>A, b => B, f => Cout);
u2: entity work.my_xor port map (a =>A, b => B, f => Sum);

end half_adder_structural;