LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.ALL;

ENTITY watch_tester IS
	PORT (
		--inputs
		CLOCK_50 : IN STD_LOGIC;
		KEY : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
		--outputs
		HEX0 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		HEX1 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		HEX2 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		HEX3 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		HEX4 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		HEX5 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0)

	);
END watch_tester;

ARCHITECTURE implementation OF watch_tester IS
BEGIN
	watch : ENTITY work.watch PORT MAP(
		clk => CLOCK_50,
		speed => KEY(0),
		reset => KEY(1),
		sec_1 => HEX0(6 DOWNTO 0),
		sec_10 => HEX1(6 DOWNTO 0),
		min_1 => HEX2(6 DOWNTO 0),
		min_10 => HEX3(6 DOWNTO 0),
		hrs_1 => HEX4(6 DOWNTO 0),
		hrs_10 => HEX5(6 DOWNTO 0),
		tm => OPEN
		);
END implementation;