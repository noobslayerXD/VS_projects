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

	-- naming signals
	signal carry1, carry2, carry3 : std_logic;

begin
-- full adder, with ports connected to signals in that order
fa1: entity work.full_adder port map (A =>A(0), B => B(0), Sum => Sum(0), Cout => carry1,Cin => Cin);
fa2: entity work.full_adder port map (A =>A(1), B => B(1), Sum => Sum(1), Cout => carry2,Cin => carry1);
fa3: entity work.full_adder port map (A =>A(2), B => B(2), Sum => Sum(2), Cout => carry3,Cin => carry2);
fa4: entity work.full_adder port map (A =>A(3), B => B(3), Sum => Sum(3), Cout => Cout, Cin => carry3);
	
end four_bit_adder_impl;