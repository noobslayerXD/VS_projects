library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity full_adder_tester is

	port
	(
		-- Input ports
	signal	SW0	: in  std_logic;
	signal	SW1	: in  std_logic;
	signal	SW2	: in  std_logic;

		-- Output ports
		LEDR0, LEDR1	: out std_logic
	);
end full_adder_tester;

architecture full_adder_tester_impl of full_adder_tester is


begin

-- To instantiate an entity directly, the entity must be written in VHDL.
-- You must also add the file containing the entity declaration to your
-- Quartus II project.
UUT: entity work.full_adder(full_adder_struct)
	
	port map 
	(
		A => SW0,
		B => SW1,
		Cin =>SW2,
		Sum =>LEDR0,
		Cout =>LEDR1
	);


end full_adder_tester_impl;

