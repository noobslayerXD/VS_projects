LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.ALL;

ENTITY code_lock_simple IS
	PORT (
		clk : IN STD_LOGIC;
		reset : IN STD_LOGIC;
		code : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
		enter : IN STD_LOGIC;
		err_count : OUT STD_LOGIC_VECTOR(1 DOWNTO 0);
		lock : OUT STD_LOGIC;
		lock0 : OUT STD_LOGIC

	);
END code_lock_simple;

ARCHITECTURE rtl OF code_lock_simple IS

	--------Interne signaler---------------------
	SIGNAL enter_sync : STD_LOGIC;
	SIGNAL failed : STD_LOGIC;
	SIGNAL err_event : STD_LOGIC;

BEGIN
	synchronizer : ENTITY work.synch PORT MAP (clk => clk, async_sig => NOT enter, rise => OPEN, fall => enter_sync); --Brug enten rise eller fall output

	fsm : ENTITY work.code_lock_simple_fsm PORT MAP (clk => clk, reset => reset, enter => enter_sync,
		code => code, lock => lock, err_event => err_event, failed => failed, lock0 => lock0);

	Wrong : ENTITY work.Wrong PORT MAP(clk => clk, reset => reset, failed => failed, err_event => err_event, err_count => err_count);
END;