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

-- To instantiate an entity directly, the entity must be written in VHDL.
-- You must also add the file containing the entity declaration to your
-- Quartus II project.



end full_adder_struct;



