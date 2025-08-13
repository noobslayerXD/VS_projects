library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.all;

entity four_bit_adder_tester is
	
	port
	(
		-- Input ports
		SW	: in  std_logic_vector(8 downto 0);

		-- Output ports
		LEDR	: out std_logic_vector(4 downto 0)
	);
end four_bit_adder_tester;


architecture four_bit_adder_tester_impl of four_bit_adder_tester is

	-- Declarations (optional)

begin

-- To instantiate an entity directly, the entity must be written in VHDL.
-- You must also add the file containing the entity declaration to your
-- Quartus II project.



end four_bit_adder_tester_impl;

