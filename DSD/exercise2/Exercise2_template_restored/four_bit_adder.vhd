library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.all;

entity four_bit_adder is

	port (
	-- Input ports
	Cin : in std_logic;
	A, B : in std_logic_vector(3 downto 0);

	-- Output ports
	Sum : out std_logic_vector(3 downto 0);
	Cout : out std_logic
	);
end four_bit_adder;

architecture four_bit_adder_impl of four_bit_adder is

	signal carry1, carry2, carry3 : std_logic;

begin

	
end four_bit_adder_impl;