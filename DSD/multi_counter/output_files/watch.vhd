LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.ALL;

ENTITY watch IS
	PORT (
		--inputs
		clk : IN STD_LOGIC; -- Clock input
		speed : IN STD_LOGIC; -- fart
		reset : IN STD_LOGIC; -- reset 

		--outputs
		sec_1 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		sec_10 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		min_1 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		min_10 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		hrs_1 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		hrs_10 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		tm : OUT STD_LOGIC_VECTOR(15 DOWNTO 0)

	);

END watch;

ARCHITECTURE watch_imp OF watch IS

	SIGNAL bcd1, bcd2, bcd3, bcd4, bcd5, bcd6 : STD_LOGIC_VECTOR(3 DOWNTO 0);
	SIGNAL carry1, carry2, carry3, carry4, carry5, carry6, reset1 : STD_LOGIC;

BEGIN
	clock_gen : ENTITY work.clock_gen PORT MAP (
		clk => clk,
		speed => speed,
		reset => reset1,
		clk_out => carry1
		);

	--sec_1
	multi_counter1 : ENTITY work.multi_counter PORT MAP (
		clken => carry1,
		clk => clk,
		reset => reset1,
		mode => "00",
		count => bcd1(3 DOWNTO 0),
		cout => carry2
		);

	bin2hex1 : ENTITY work.bin2hex PORT MAP (
		bin => bcd1(3 DOWNTO 0),
		seg => sec_1(6 DOWNTO 0)
		);

	--sec_10
	multi_counter2 : ENTITY work.multi_counter PORT MAP (
		clken => carry2,
		clk => clk,
		reset => reset1,
		mode => "01",
		count => bcd2(3 DOWNTO 0),
		cout => carry3
		);

	bin2hex2 : ENTITY work.bin2hex PORT MAP (
		bin => bcd2(3 DOWNTO 0),
		seg => sec_10(6 DOWNTO 0)
		);
	--min_1	
	multi_counter3 : ENTITY work.multi_counter PORT MAP (
		clken => carry3,
		clk => clk,
		reset => reset1,
		mode => "00",
		count => bcd3(3 DOWNTO 0),
		cout => carry4
		);

	bin2hex3 : ENTITY work.bin2hex PORT MAP (
		bin => bcd3(3 DOWNTO 0),
		seg => min_1(6 DOWNTO 0)
		);
	--min_10	
	multi_counter4 : ENTITY work.multi_counter PORT MAP (
		clken => carry4,
		clk => clk,
		reset => reset1,
		mode => "01",
		count => bcd4(3 DOWNTO 0),
		cout => carry5
		);

	bin2hex4 : ENTITY work.bin2hex PORT MAP (
		bin => bcd4(3 DOWNTO 0),
		seg => min_10(6 DOWNTO 0)
		);
	--hrs_1	
	multi_counter5 : ENTITY work.multi_counter PORT MAP (
		clken => carry5,
		clk => clk,
		reset => reset1,
		mode => "00",
		count => bcd5(3 DOWNTO 0),
		cout => carry6
		);

	bin2hex5 : ENTITY work.bin2hex PORT MAP (
		bin => bcd5(3 DOWNTO 0),
		seg => hrs_1(6 DOWNTO 0)
		);
	--hrs_10	
	multi_counter6 : ENTITY work.multi_counter PORT MAP (
		clken => carry6,
		clk => clk,
		reset => reset1,
		mode => "11",
		count => bcd6(3 DOWNTO 0),
		cout => OPEN
		);

	bin2hex6 : ENTITY work.bin2hex PORT MAP (
		bin => bcd6(3 DOWNTO 0),
		seg => hrs_10(6 DOWNTO 0)
		);

	reset_logic : ENTITY work.reset_logic PORT MAP (
		reset_out => reset1,
		clk => clk,
		reset_in => reset,
		hrs_bin1 => bcd5(3 DOWNTO 0),
		hrs_bin10 => bcd6(3 DOWNTO 0)
		);

	-- tm
	tm (15 DOWNTO 12) <= bcd6;
	tm (11 DOWNTO 8) <= bcd5;
	tm (7 DOWNTO 4) <= bcd4;
	tm (3 DOWNTO 0) <= bcd3;
END watch_imp;