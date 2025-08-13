LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.ALL;

ENTITY alarm_watch_tester IS
	PORT (
		--inputs
		KEY : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
		SW : IN STD_LOGIC_VECTOR(15 DOWNTO 0);
		CLOCK_50 : IN STD_LOGIC;
		--outputs
		LEDR : OUT STD_LOGIC_VECTOR(0 DOWNTO 0);
		HEX0 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		HEX1 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		HEX2 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		HEX3 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		HEX4 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		HEX5 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0)
	);
END alarm_watch_tester;

ARCHITECTURE Behavioral OF alarm_watch_tester IS
BEGIN
	alarm_watch : ENTITY work.alarm_watch PORT MAP(
		clk => CLOCK_50,
		set_speed => KEY(0),
		resets => KEY(1),
		--		set_min1 => SW(3 downto 0),
		--		set_min10 => SW(7 downto 4),
		--		set_hrs1 => SW(11 downto 8),
		--		set_hrs10 => SW(15 downto 12),
		-- delete from here
		set_min1 => SW(3 DOWNTO 0),
		set_min10 => SW(7 DOWNTO 4),
		set_hrs1(1 DOWNTO 0) => SW(9 DOWNTO 8),
		set_hrs1 (3 DOWNTO 2) => "00",
		set_hrs10 => "0000",
		-- to here
		sec_1 => HEX0(6 DOWNTO 0),
		sec_10 => HEX1(6 DOWNTO 0),
		min_1 => HEX2(6 DOWNTO 0),
		min_10 => HEX3(6 DOWNTO 0),
		hrs_1 => HEX4(6 DOWNTO 0),
		hrs_10 => HEX5(6 DOWNTO 0),
		alarm => LEDR(0)
		);

END Behavioral;