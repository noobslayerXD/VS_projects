LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.ALL;

ENTITY one_digit_clock_tester IS
	PORT (
		--inputs
		KEY : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
		SW : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
		CLOCK_50 : IN STD_LOGIC;
		--outputs
		HEX0 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		LEDR : OUT STD_LOGIC
	);
END one_digit_clock_tester;

ARCHITECTURE implementation OF one_digit_clock_tester IS

	SIGNAL multi : STD_LOGIC_VECTOR(3 DOWNTO 0);
	SIGNAL klok : STD_LOGIC;

BEGIN

	bin2hex : ENTITY work.bin2hex PORT MAP (
		bin => multi(3 DOWNTO 0),
		seg => HEX0(6 DOWNTO 0)
		);
	multi_counter : ENTITY work.multi_counter PORT MAP (
		clken => klok,
		clk => CLOCK_50,
		reset => KEY(1),
		mode => SW(1 DOWNTO 0),
		count => multi(3 DOWNTO 0),
		cout => LEDR
		);

	clock_gen : ENTITY work.clock_gen PORT MAP (
		clk => CLOCK_50,
		speed => KEY(0),
		reset => KEY(1),
		clk_out => klok
		);
END implementation;