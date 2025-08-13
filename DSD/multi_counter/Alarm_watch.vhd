LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.ALL;

ENTITY alarm_watch IS
	PORT (
		--inputs
		set_min1 : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
		set_min10 : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
		set_hrs1 : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
		set_hrs10 : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
		clk : IN STD_LOGIC;
		set_speed : IN STD_LOGIC;
		resets : IN STD_LOGIC;
		--outputs
		alarm : OUT STD_LOGIC;
		sec_1 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		sec_10 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		min_1 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		min_10 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		hrs_1 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		hrs_10 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0)
	);
END alarm_watch;

ARCHITECTURE Behavioral OF alarm_watch IS
	SIGNAL alarm_signal, timer_signal : STD_LOGIC_VECTOR(15 DOWNTO 0);

BEGIN
	watch : ENTITY work.watch PORT MAP(
		clk => clk,
		speed => set_speed,
		reset => resets,
		sec_1 => sec_1,
		sec_10 => sec_10,
		min_1 => min_1,
		min_10 => min_10,
		hrs_1 => hrs_1,
		hrs_10 => hrs_10,
		tm => timer_signal
		);

	inputLimiter : ENTITY work.InputLimiter PORT MAP (
		bin_min1 => set_min1,
		bin_min10 => set_min10,
		bin_hrs1 => set_hrs1,
		bin_hrs10 => set_hrs10,
		time_alarm => alarm_signal
		);

	compare : ENTITY work.Compare PORT MAP (
		tm_watch => timer_signal,
		tm_alarm => alarm_signal,
		alarm => alarm
		);

END Behavioral;