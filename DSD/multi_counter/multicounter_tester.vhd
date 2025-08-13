LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.ALL;

ENTITY multicounter_tester IS
	PORT (
		--inputs
		KEY : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
		SW : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
		--outputs
		HEX0 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		LEDR : OUT STD_LOGIC
	);
END multicounter_tester;

ARCHITECTURE implementation OF multicounter_tester IS

	SIGNAL multi : STD_LOGIC_VECTOR(3 DOWNTO 0);

BEGIN

	bin2hex : ENTITY work.bin2hex PORT MAP (
		bin => multi(3 DOWNTO 0),
		seg => HEX0(6 DOWNTO 0)
		);
	multi_counter : ENTITY work.multi_counter PORT MAP (
		clken => '1',
		clk => KEY(0),
		reset => KEY(1),
		mode => SW(1 DOWNTO 0),
		count => multi(3 DOWNTO 0),
		cout => LEDR
		);
END implementation;